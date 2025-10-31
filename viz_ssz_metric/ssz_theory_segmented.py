#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSZ — Wirkungsbasiert (Skalar mit anisotroper Kinetik) — stabil (v2)
- Fundamentale Materie-Wirkung mit richtungsselektiver Kinetik (Z_parallel)
- Feldgrößen (ρ_φ, p_r,φ, p_t,φ, Δ_φ) aus der Wirkung
- TOV + Skalar-EOM im SSS-Fall
- Numerisch stabil: ln(r)-Integration, sech^2-stabil, exp-Clipping, tanh-Sättigungen
- Integrator: LSODA (robust), Fallback Radau
- Physik-Modi: exterior (Vakuum + m0=r_s/2) | interior (Fluid)
"""

import math
import argparse
from dataclasses import dataclass
from typing import Tuple, List
import numpy as np
from scipy.integrate import solve_ivp
import csv
import sys

# --------------------------- Physikalische Konstanten ---------------------------

G_SI = 6.67430e-11           # m^3 / (kg s^2)
C_SI = 299_792_458.0         # m / s

def mass_to_length_geom(M_kg: float) -> float:
    """In geometrischen Einheiten (G=c=1): m_geom = G M / c^2"""
    return G_SI * M_kg / (C_SI**2)

# --------------------------- Numerische Hilfsfunktionen -------------------------

def sech2_stable(z: float) -> float:
    """sech^2(z) stabil, vermeidet Overflow in cosh."""
    a = abs(z)
    if a < 20.0:
        c = math.cosh(z)
        return 1.0 / (c * c)
    # cosh(z) ~ 0.5 e^{|z|}  =>  sech^2 ~ 4 e^{-2|z|}
    return 4.0 * math.exp(-2.0 * a)

def exp_clip(x: float, bound: float = 80.0) -> float:
    """Geklipptes Exponential: exp(x) mit |x|≤bound."""
    if x >  bound: x =  bound
    if x < -bound: x = -bound
    return math.exp(x)

def sat(x: float, cap: float | None) -> float:
    """Glatte Sättigung ±cap via tanh."""
    if cap is None or cap <= 0:
        return x
    return cap * math.tanh(x / cap)

def sat_pos(y: float, cap: float | None) -> float:
    """Glatte Sättigung y≥0 gegen cap via tanh."""
    if cap is None or cap <= 0:
        return max(y, 0.0)
    return cap * math.tanh(max(y, 0.0) / cap)

# --------------------------- Modellfunktionen: Z_parallel & U -------------------

def Zpar_raw(phi_eff: float, Z0: float, alpha: float, beta: float) -> float:
    """Ungeklammerte Z_parallel(φ_eff)."""
    return Z0 * (1.0 + alpha * phi_eff + beta * phi_eff * phi_eff)

def Zpar(phi: float, Z0: float, alpha: float, beta: float, phi_cap: float,
         Zmin: float, Zmax: float) -> float:
    """Z_parallel(φ) = clamp( Z0 * [1 + α sat(φ) + β sat(φ)^2], Zmin, Zmax )"""
    ph = sat(phi, phi_cap)
    z  = Zpar_raw(ph, Z0, alpha, beta)
    if z < Zmin: z = Zmin
    if z > Zmax: z = Zmax
    return z

def dZpar_dphi(phi: float, Z0: float, alpha: float, beta: float, phi_cap: float,
               Zmin: float, Zmax: float) -> float:
    """
    d/dφ Z_parallel(φ) mit gesättigtem φ.
    d/dφ sat(φ) = sech^2(φ/φ_cap). Ableitung wird an den Klammern Zmin/Zmax saturiert (≈0 am Rand).
    """
    if phi_cap is None or phi_cap <= 0:
        # ohne Caps: einfache Ableitung, aber clamp auf [Zmin,Zmax] (flache Ableitung außerhalb)
        z = Zpar_raw(phi, Z0, alpha, beta)
        if z <= Zmin or z >= Zmax:
            return 0.0
        return Z0 * (alpha + 2.0 * beta * phi)

    ph  = sat(phi, phi_cap)          # = φ_cap * tanh(φ/φ_cap)
    z   = Zpar_raw(ph, Z0, alpha, beta)
    if z <= Zmin or z >= Zmax:
        return 0.0
    dph = sech2_stable(phi / phi_cap)  # d/dφ sat(φ) = sech^2(φ/φ_cap)
    return Z0 * (alpha + 2.0 * beta * ph) * dph

def U(phi: float, mphi: float, lam: float, phi_cap: float) -> float:
    """U(φ) = 1/2 m^2 sat(φ)^2 + λ sat(φ)^4"""
    ph = sat(phi, phi_cap)
    return 0.5 * (mphi**2) * ph * ph + lam * (ph**4)

def dU_dphi(phi: float, mphi: float, lam: float, phi_cap: float) -> float:
    """dU/dφ mit Kettenregel (sat)."""
    if phi_cap is None or phi_cap <= 0:
        return (mphi**2) * phi + 4.0 * lam * (phi**3)
    ph  = sat(phi, phi_cap)
    dph = sech2_stable(phi / phi_cap)
    return ((mphi**2) * ph + 4.0 * lam * (ph**3)) * dph

# --------------------------- Parameter & RHS ------------------------------------

@dataclass
class Params:
    # Skalar-Kinetik
    Z0: float
    alpha: float
    beta: float
    Zmin: float
    Zmax: float
    # Skalar-Potential
    mphi: float
    lam: float
    # Sättigungen
    phi_cap: float
    phip_cap: float
    # Fluid EoS
    cs2: float
    rho0: float
    # Horizon guard
    abort_on_horizon: bool
    horizon_margin: float

class HorizonError(RuntimeError):
    pass

def rhs_dr(r: float, y: np.ndarray, p: Params) -> np.ndarray:
    """
    dy/dr = f(r,y). y = [m, Phi, pr_fluid, phi, phip]
    """
    m, Phi, pr_fl, phi, phip = (float(y[0]), float(y[1]), float(y[2]), float(y[3]), float(y[4]))

    r_safe = max(r, 1e-30)
    one_minus = 1.0 - 2.0 * m / r_safe
    if p.abort_on_horizon and (one_minus <= p.horizon_margin):
        raise HorizonError(f"Horizontwächter: 1-2m/r={one_minus:.3e} < margin={p.horizon_margin:.1e} bei r={r:.6e} m.")

    # weich clippen (bleibe >0 für numerische Stabilität, physik. Bewertung via Guard)
    if one_minus < 1e-16:
        one_minus = 1e-16

    Lam = -0.5 * math.log(one_minus)   # e^{2Λ} = 1/(1-2m/r),  e^{-2Λ} = 1-2m/r
    inv_e2L = one_minus

    # Skalar-Sektor
    Zp    = Zpar(phi, p.Z0, p.alpha, p.beta, p.phi_cap, p.Zmin, p.Zmax)
    Up    = U(phi, p.mphi, p.lam, p.phi_cap)
    phip_s = sat(phip, p.phip_cap)
    X     = inv_e2L * (phip_s**2)

    rho_phi =  0.5 * Zp * X + Up
    pr_phi  =  0.5 * Zp * X - Up
    pt_phi  = -0.5 * Zp * X - Up
    Delta_phi = pt_phi - pr_phi               # = -Zp * X

    # Fluid (isotrop)
    cs2 = max(p.cs2, 1e-16)
    rho_fl = (pr_fl / cs2) + p.rho0
    pt_fl  = pr_fl

    # Summen
    rho_tot = rho_fl + rho_phi
    pr_tot  = pr_fl + pr_phi

    # TOV
    denom = r_safe * (r_safe - 2.0 * m)
    if abs(denom) < 1e-18 * r_safe * r_safe:
        denom = math.copysign(1e-18 * r_safe * r_safe, denom)

    dPhidr = (m + 4.0 * math.pi * (r_safe**3) * pr_tot) / denom
    dmdr   = 4.0 * math.pi * (r_safe**2) * rho_tot

    # Fluiddruck
    dpr_dr = -(rho_fl + pr_fl) * dPhidr + (2.0 / r_safe) * (pt_fl - pr_fl + Delta_phi)

    # Skalar-EOM explizit:
    Zphi   = dZpar_dphi(phi, p.Z0, p.alpha, p.beta, p.phi_cap, p.Zmin, p.Zmax)
    source = dU_dphi(phi, p.mphi, p.lam, p.phi_cap) + 0.5 * Zphi * X

    ePhi_m_L = exp_clip(Phi - Lam, 80.0)
    ePhi_p_L = exp_clip(Phi + Lam, 80.0)

    A = ePhi_m_L * (r_safe**2) * max(Zp, 1e-16)
    B = ePhi_p_L * (r_safe**2) * source

    # Λ' = (m + 4π r^3 ρ_tot)/(r(r-2m))
    dLdr = (m + 4.0 * math.pi * (r_safe**3) * rho_tot) / denom
    # A' = A*(Φ' - Λ' + 2/r) + e^{Φ-Λ} r^2 Z_{,φ} φ'_sat
    Aprime = A * (dPhidr - dLdr + 2.0 / r_safe) + ePhi_m_L * (r_safe**2) * Zphi * phip_s

    dphipdr = (B - Aprime * phip) / max(A, 1e-30)

    return np.array([dmdr, dPhidr, dpr_dr, phip, dphipdr], dtype=float)

# --------------------------- Integration & Export -------------------------------

def integrate_theory(rmin: float, rmax: float, y0: np.ndarray, p: Params,
                     coord: str, max_step_r: float | None) -> Tuple[np.ndarray, np.ndarray]:
    """
    Integration in r oder x=ln r. Rückgabe: (r_nodes, Y_nodes)
    """
    kwargs = dict(rtol=1e-7, atol=1e-9, vectorized=False)
    if coord == "r":
        if max_step_r is not None and max_step_r > 0:
            kwargs["max_step"] = max_step_r

        # 1) LSODA
        try:
            sol = solve_ivp(lambda rr, y: rhs_dr(rr, y, p), (rmin, rmax), y0, method="LSODA", **kwargs)
            if sol.success and len(sol.t) >= 2:
                return sol.t, sol.y
        except HorizonError as he:
            raise he
        except Exception:
            pass

        # 2) Radau
        sol = solve_ivp(lambda rr, y: rhs_dr(rr, y, p), (rmin, rmax), y0, method="Radau", **kwargs)
        if not sol.success or len(sol.t) < 2:
            raise RuntimeError(f"Integrator fehlgeschlagen: {sol.message}")
        return sol.t, sol.y

    # coord == "lnr"
    xmin = math.log(rmin)
    xmax = math.log(rmax)
    dx_max = None
    if max_step_r is not None and max_step_r > 0:
        # konservativ am Startwert rmin binden
        dx_max = max_step_r / rmin
        kwargs["max_step"] = dx_max

    def rhs_dx(x: float, y: np.ndarray) -> np.ndarray:
        r = math.exp(x)
        dy_dr = rhs_dr(r, y, p)
        return r * dy_dr  # dy/dx = r * dy/dr

    # 1) LSODA
    try:
        sol = solve_ivp(rhs_dx, (xmin, xmax), y0, method="LSODA", **kwargs)
        if sol.success and len(sol.t) >= 2:
            r_nodes = np.exp(sol.t)
            return r_nodes, sol.y
    except HorizonError as he:
        raise he
    except Exception:
        pass

    # 2) Radau
    sol = solve_ivp(rhs_dx, (xmin, xmax), y0, method="Radau", **kwargs)
    if not sol.success or len(sol.t) < 2:
        raise RuntimeError(f"Integrator fehlgeschlagen (ln r): {sol.message}")
    r_nodes = np.exp(sol.t)
    return r_nodes, sol.y

def interpolate_solution(t_src: np.ndarray, Y_src: np.ndarray, t_dst: np.ndarray) -> np.ndarray:
    """Lineare Interpolation Y(t) auf t_dst."""
    Y_dst = np.zeros((Y_src.shape[0], len(t_dst)), dtype=float)
    for i in range(Y_src.shape[0]):
        Y_dst[i, :] = np.interp(t_dst, t_src, Y_src[i, :])
    return Y_dst

def build_rows(r_grid: np.ndarray, Y: np.ndarray, p: Params, rs: float) -> Tuple[List[str], List[List[float]]]:
    header = [
        "r_over_rs", "r_m", "m_geom_m", "Phi",
        "rho_fl", "pr_fl", "pt_fl",
        "phi", "phip",
        "Zpar", "U",
        "X", "rho_phi", "pr_phi", "pt_phi", "Delta_phi",
        "rho_tot", "pr_tot", "pt_tot", "one_minus_2m_over_r"
    ]
    rows: List[List[float]] = []
    for k in range(len(r_grid)):
        r = float(r_grid[k])
        m, Phi, pr_fl, phi, phip = (float(Y[0,k]), float(Y[1,k]), float(Y[2,k]), float(Y[3,k]), float(Y[4,k]))
        one_minus = max(1.0 - 2.0 * m / max(r, 1e-30), 1e-16)

        Lam = -0.5 * math.log(one_minus)
        inv_e2L = one_minus

        Zp  = Zpar(phi, p.Z0, p.alpha, p.beta, p.phi_cap, p.Zmin, p.Zmax)
        Up  = U(phi, p.mphi, p.lam, p.phi_cap)
        phip_s = sat(phip, p.phip_cap)
        X   = inv_e2L * (phip_s**2)

        rho_phi =  0.5 * Zp * X + Up
        pr_phi  =  0.5 * Zp * X - Up
        pt_phi  = -0.5 * Zp * X - Up
        Delta_phi = pt_phi - pr_phi

        rho_fl = (pr_fl / max(p.cs2, 1e-16)) + p.rho0
        pt_fl  = pr_fl

        rho_tot = rho_fl + rho_phi
        pr_tot  = pr_fl + pr_phi
        pt_tot  = pt_fl + pt_phi

        rows.append([
            r/rs, r, m, Phi,
            rho_fl, pr_fl, pt_fl,
            phi, phip,
            Zp, Up,
            X, rho_phi, pr_phi, pt_phi, Delta_phi,
            rho_tot, pr_tot, pt_tot, one_minus
        ])
    return header, rows

def write_csv(path: str, header: List[str], rows: List[List[float]]) -> None:
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        for row in rows:
            out = []
            for x in row:
                if isinstance(x, float):
                    out.append(f"{x:.10e}")
                else:
                    out.append(x)
            w.writerow(out)

# --------------------------- CLI & Main ----------------------------------------

def main():
    ap = argparse.ArgumentParser(description="SSZ (Action-basiert, stabil) — Scalar + anisotrope Kinetik")
    ap.add_argument("--M", type=float, required=True, help="Masse in kg")
    ap.add_argument("--mode", choices=["exterior","interior"], default="exterior",
                    help="exterior: Vakuum + m0=r_s/2, interior: Fluid aktiv")
    ap.add_argument("--coord", choices=["r","lnr"], default="lnr", help="Integrationskoordinate")
    ap.add_argument("--rmin-mult", type=float, default=1.05, help="r_min = mult * r_s")
    ap.add_argument("--rmax-mult", type=float, default=12.0, help="r_max = mult * r_s")
    ap.add_argument("--grid", type=int, default=200, help="Anzahl Rasterpunkte für Ausgabe")
    ap.add_argument("--export", type=str, default="out_theory.csv", help="Ausgabe-CSV")

    # Anfangswerte
    ap.add_argument("--phi0", type=float, default=1e-4)
    ap.add_argument("--phip0", type=float, default=0.0)
    ap.add_argument("--pr0", type=float, default=0.0)
    ap.add_argument("--m0", type=float, default=None, help="optional: Startwert m(rmin) in geometrischen Metern")

    # Skalar-Parameter
    ap.add_argument("--mphi", type=float, default=0.0)
    ap.add_argument("--lam", type=float, default=0.0)
    ap.add_argument("--Z0", type=float, default=1.0)
    ap.add_argument("--alpha", type=float, default=3e-3)
    ap.add_argument("--beta", type=float, default=-8e-3)
    ap.add_argument("--Zmin", type=float, default=1e-8)
    ap.add_argument("--Zmax", type=float, default=1e+8)

    # Sättigungs-Caps
    ap.add_argument("--phi-cap", type=float, default=1e-3)
    ap.add_argument("--phip-cap", type=float, default=1e-3)

    # Fluid
    ap.add_argument("--cs2", type=float, default=0.30)
    ap.add_argument("--rho0", type=float, default=0.0)

    # Integrator
    ap.add_argument("--max-step-rs", type=float, default=0.02, help="max_step relativ zu r_s (0 = kein Limit)")

    # Horizont-Wächter
    ap.add_argument("--abort-on-horizon", action="store_true", default=True)
    ap.add_argument("--horizon-margin", type=float, default=1e-6)

    # (Nur Print) Kompat: frühere Seg.-Parameter (keine Funktion hier)
    ap.add_argument("--seg-frac", type=float, default=0.6)
    ap.add_argument("--seg-scale", type=str, choices=["r_s","r_phi","auto"], default="r_phi")
    ap.add_argument("--kernel", type=str, choices=["gauss","exp","box"], default="gauss")
    ap.add_argument("--eps3", type=float, default=-4.8)
    ap.add_argument("--rphi-hint", type=float, default=None)

    args = ap.parse_args()

    # Geometrische Längen
    m_geom = mass_to_length_geom(args.M)     # in m (geom)
    r_s = 2.0 * m_geom
    rmin = args.rmin_mult * r_s
    rmax = args.rmax_mult * r_s
    if not (rmax > rmin > 0):
        print("[fatal] Ungültiger Bereich: rmin<rmax und >0 erforderlich.", file=sys.stderr)
        sys.exit(2)

    print("="*80)
    print("SSZ — Wirkungsbasiert (Skalar mit anisotroper Kinetik) — stabil (v2)")
    print("="*80)
    print(f"M = {args.M: .6e} kg | r_s = {r_s: .6e} m")
    print(f"[grid] r/rs in [{args.rmin_mult:.2f}, {args.rmax_mult:.2f}] mit {args.grid} Punkten")
    print(f"[mode] {args.mode} | coord={args.coord}")
    print(f"[Zpar] Z0={args.Z0:g} α={args.alpha:g} β={args.beta:g} | caps: φ={args.phi_cap:g}, φ'={args.phip_cap:g} | clamp: Z∈[{args.Zmin:g},{args.Zmax:g}]")
    print(f"[fluid] cs2={args.cs2:.3f} rho0={args.rho0: .3e} | pr0={args.pr0: .3e}")
    print(f"[guard] abort_on_horizon={args.abort_on_horizon} margin={args.horizon_margin: .1e}")
    print(f"[compat] seg_frac={args.seg_frac} seg_scale={args.seg_scale} kernel={args.kernel} eps3={args.eps3}")

    # Mode-abhängige Defaults
    pr0 = args.pr0
    rho0 = args.rho0
    if args.mode == "exterior":
        rho0 = 0.0
        pr0  = 0.0

    # Startwerte
    if args.m0 is not None:
        m0 = float(args.m0)
    else:
        if args.mode == "exterior":
            # Exterieur: Schwarzschild-Masse bereits da
            m0 = 0.5 * r_s
        else:
            # Interior: konservativ klein, damit 2m/r << 1 am Rand
            m0 = min(1e-6 * m_geom, 0.05 * rmin)

    if 2.0 * m0 / rmin > 0.9:
        print(f"[warn] m0 groß relativ zu rmin: 2m/r = {2.0*m0/rmin:.3f}")

    Phi0  = 0.0
    phi0  = args.phi0
    phip0 = args.phip0

    y0 = np.array([m0, Phi0, pr0, phi0, phip0], dtype=float)

    p = Params(
        Z0=args.Z0, alpha=args.alpha, beta=args.beta, Zmin=args.Zmin, Zmax=args.Zmax,
        mphi=args.mphi, lam=args.lam,
        phi_cap=args.phi_cap, phip_cap=args.phip_cap,
        cs2=args.cs2, rho0=rho0,
        abort_on_horizon=bool(args.abort_on_horizon), horizon_margin=args.horizon_margin
    )

    max_step_r = None
    if args.max_step_rs and args.max_step_rs > 0:
        max_step_r = args.max_step_rs * r_s

    # Integration
    try:
        r_nodes, Y_nodes = integrate_theory(rmin, rmax, y0, p, coord=args.coord, max_step_r=max_step_r)
    except HorizonError as he:
        print(f"[fatal] {he}", file=sys.stderr)
        sys.exit(3)

    # Ausgabe-Raster & Interpolation
    r_grid = np.linspace(rmin, rmax, args.grid)
    Y_grid = interpolate_solution(r_nodes, Y_nodes, r_grid)

    # CSV
    header, rows = build_rows(r_grid, Y_grid, p, r_s)
    write_csv(args.export, header, rows)
    print(f"\n[ok] CSV: {args.export}")

if __name__ == "__main__":
    main()

