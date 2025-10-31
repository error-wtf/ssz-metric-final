# -*- coding: utf-8 -*-
"""
SSZ Metric Visualization CLI

Generates plots and animated GIFs for the SSZ mirror metric.

© 2025 Carmen Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
import argparse
import io
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from .ssz_mirror_metric import (
    A_GR, A_SSZ, A_safe, D_from_A, redshift_from_A, curvature_proxy, solve_r_star, PHI
)

# UTF-8 encoding for Windows (prevents UnicodeEncodeError with Greek letters)
os.environ['PYTHONIOENCODING'] = 'utf-8:replace'
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except AttributeError:
        # Python < 3.7 fallback
        if hasattr(sys.stdout, 'buffer'):
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)

OUTDIR = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUTDIR, exist_ok=True)


def _save_gif(frames, path, duration=130):
    """Save list of PIL images as animated GIF."""
    frames[0].save(
        path, save_all=True, append_images=frames[1:], 
        optimize=True, duration=duration, loop=0
    )
    print(f"✅ GIF saved: {path}")


def cmd_check(rs: float, varphis):
    """Check intersection points for different φ values."""
    from .ssz_mirror_metric import solve_r_star, D_SSZ
    
    print("\n" + "="*80)
    print("SSZ-GR INTERSECTION CHECK")
    print("="*80)
    
    for v in varphis:
        rstar = solve_r_star(rs, v)
        u_star = rstar / rs
        
        # Calculate D at intersection
        D_ssz = D_SSZ(rstar, rs, v)
        D_gr = np.sqrt(1 - rs/rstar)
        
        print(f"\nφ = {v:.10f}")
        print(f"  u* = r*/r_s = {u_star:.10f}")
        print(f"  r* = {rstar:.6e} (in units of r_s)")
        print(f"  D*(SSZ) = {D_ssz:.10f}")
        print(f"  D*(GR)  = {D_gr:.10f}")
        print(f"  |Diff|  = {abs(D_ssz - D_gr):.2e}")
    
    print("\n" + "="*80)


def gif_time_dilation(rs: float, varphi: float, outname="time_dilation_mirror_phi.gif"):
    """Animate time dilation D(r) with φ-sweep."""
    r = np.linspace(1.05*rs, 6.0*rs, 600)
    frames = []
    
    # Sweep φ from 0.8*φ to 1.25*φ
    phi_values = np.linspace(varphi*0.8, varphi*1.25, 22)
    
    for v in phi_values:
        Agr = A_GR(r, rs)
        Assz = A_SSZ(r, rs, v)
        Asafe, rstar = A_safe(r, rs, varphi=v)
        
        fig, ax = plt.subplots(figsize=(6.4, 3.9), dpi=120)
        ax.plot(r/rs, D_from_A(Agr),  label="GR", lw=2, color='#1f77b4')
        ax.plot(r/rs, D_from_A(Assz), label="SSZ", lw=2, ls="--", color='#ff7f0e')
        ax.plot(r/rs, D_from_A(Asafe), label="Mirror (safe)", lw=2.5, color='#2ca02c')
        ax.axvline(rstar/rs, ls=":", lw=1.6, color='red', alpha=0.7)
        ax.text(rstar/rs + 0.02, 0.1, r"$r^\ast$", fontsize=10)
        
        ax.set(xlabel=r"$r/r_s$", ylabel=r"$D(r)$", 
               xlim=(1.05, 6.0), ylim=(0, 1.05),
               title=f"Time Dilation — φ = {v:.3f}")
        ax.grid(alpha=0.25)
        ax.legend(loc="lower right", fontsize=8)
        
        buf = io.BytesIO()
        plt.tight_layout()
        fig.savefig(buf, format="png")
        plt.close(fig)
        buf.seek(0)
        frames.append(Image.open(buf).convert("P"))
    
    _save_gif(frames, os.path.join(OUTDIR, outname), duration=140)


def gif_A_compare(rs: float, varphi=PHI, outname="A_safe_comparison.gif"):
    """Animate A(r) comparison with moving marker."""
    r = np.linspace(1.05*rs, 4.0*rs, 500)
    Agr  = A_GR(r, rs)
    Assz = A_SSZ(r, rs, varphi)
    Asafe, rstar = A_safe(r, rs, varphi=varphi)
    
    ymin = min(Agr.min(), Assz.min(), Asafe.min()) * 1.1
    frames = []
    
    indices = np.linspace(0, len(r)-1, 36, dtype=int)
    
    for i in indices:
        fig, ax = plt.subplots(figsize=(6.4, 3.9), dpi=120)
        ax.plot(r/rs, Agr,  label=r"$A_{GR}$", lw=2, color='#1f77b4')
        ax.plot(r/rs, Assz, label=r"$A_{SSZ}$", lw=2, ls="--", color='#ff7f0e')
        ax.plot(r/rs, Asafe, label=r"$A_{safe}$ (mirror)", lw=2.5, color='#2ca02c')
        ax.scatter([r[i]/rs], [Asafe[i]], s=80, c='red', zorder=5, edgecolors='darkred', linewidths=2)
        ax.axvline(rstar/rs, ls=":", lw=1.6, color='gray', alpha=0.7)
        
        ax.set(xlabel=r"$r/r_s$", ylabel=r"$A(r)$", 
               xlim=(1.05, 4.0), ylim=(ymin, 1.02),
               title=f"Metric Coefficient A(r) — marker @ r = {r[i]/rs:.2f}$r_s$")
        ax.grid(alpha=0.25)
        ax.legend(loc="lower right", fontsize=8)
        
        buf = io.BytesIO()
        plt.tight_layout()
        fig.savefig(buf, format="png")
        plt.close(fig)
        buf.seek(0)
        frames.append(Image.open(buf).convert("P"))
    
    _save_gif(frames, os.path.join(OUTDIR, outname), duration=120)


def gif_curvature_proxy(rs: float, varphi=PHI, outname="curvature_proxy_scan.gif"):
    """Animate curvature proxy scan."""
    r = np.linspace(1.05*rs, 6.0*rs, 700)
    Asafe, rstar = A_safe(r, rs, varphi=varphi)
    K = curvature_proxy(r, Asafe)
    K = K / (K.max() if K.max() > 0 else 1.0)  # Normalize
    
    frames = []
    indices = np.linspace(0, len(r)-1, 50, dtype=int)
    
    for i in indices:
        fig, ax = plt.subplots(2, 1, figsize=(6.4, 5.0), dpi=120, sharex=True)
        
        # Top: A_safe
        ax[0].plot(r/rs, Asafe, lw=2.5, color='#2ca02c')
        ax[0].scatter([r[i]/rs], [Asafe[i]], s=60, c='red', zorder=5, edgecolors='darkred', linewidths=1.5)
        ax[0].axvline(rstar/rs, ls=":", lw=1.6, color='gray', alpha=0.7)
        ax[0].set(xlim=(1.05, 6.0), ylim=(Asafe.min()*0.95, 1.02), 
                  ylabel=r"$A_{safe}$",
                  title="Mirror Metric — Curvature Proxy")
        ax[0].grid(alpha=0.25)
        
        # Bottom: Curvature proxy
        ax[1].plot(r/rs, K, lw=2, color='#d62728')
        ax[1].scatter([r[i]/rs], [K[i]], s=60, c='red', zorder=5, edgecolors='darkred', linewidths=1.5)
        ax[1].set(xlabel=r"$r/r_s$", ylabel="K (normalized)", 
                  xlim=(1.05, 6.0), ylim=(-0.02, 1.05))
        ax[1].grid(alpha=0.25)
        
        buf = io.BytesIO()
        plt.tight_layout()
        fig.savefig(buf, format="png")
        plt.close(fig)
        buf.seek(0)
        frames.append(Image.open(buf).convert("P"))
    
    _save_gif(frames, os.path.join(OUTDIR, outname), duration=120)


def gif_lens(rs: float, varphi=PHI, outname="lensing_paths.gif"):
    """
    Animate light rays (null geodesics) through the SSZ metric.
    Shows gravitational lensing with different impact parameters.
    """
    from .geodesics import GeodesicIntegrator
    from .unified_metric import UnifiedSSZMetric
    
    # Create metric (use standard mass for visualization)
    M_test = 2e30  # ~1 solar mass
    metric = UnifiedSSZMetric(mass=M_test)
    metric.r_s = rs  # Override for visualization
    integrator = GeodesicIntegrator(metric)
    
    # Different impact parameters
    b_values = np.linspace(1.5*rs, 5*rs, 8)
    
    frames = []
    
    # Animate by highlighting different rays
    for b_highlight in b_values:
        fig, ax = plt.subplots(figsize=(6, 6), dpi=120, subplot_kw=dict(projection='polar'))
        
        for b in b_values:
            # Initial conditions for photon at r0 = 50rs
            r0 = 50 * rs
            # Approximation: photon with impact parameter b
            # v_phi ≈ b / r0
            v_phi = b / r0
            
            # Simplified null geodesic (just for visualization)
            # In reality would integrate full geodesic equations
            phi_vals = np.linspace(0, np.pi, 200)
            r_vals = b / np.sin(phi_vals + 1e-3)  # Simplified trajectory
            r_vals = np.clip(r_vals, 1.01*rs, 100*rs)
            
            # Plot styling
            alpha = 1.0 if abs(b - b_highlight) < 0.1*rs else 0.3
            lw = 2.5 if abs(b - b_highlight) < 0.1*rs else 1.0
            color = 'red' if abs(b - b_highlight) < 0.1*rs else 'blue'
            
            ax.plot(phi_vals, r_vals/rs, alpha=alpha, lw=lw, color=color)
        
        # Add horizon circle
        circle_phi = np.linspace(0, 2*np.pi, 100)
        circle_r = np.ones_like(circle_phi)
        ax.plot(circle_phi, circle_r, 'k--', lw=2, label='Horizon')
        
        ax.set(ylim=(0, 10), 
               title=f"Gravitational Lensing — b = {b_highlight/rs:.2f} $r_s$")
        ax.grid(alpha=0.3)
        
        buf = io.BytesIO()
        plt.tight_layout()
        fig.savefig(buf, format="png")
        plt.close(fig)
        buf.seek(0)
        frames.append(Image.open(buf).convert("P"))
    
    _save_gif(frames, os.path.join(OUTDIR, outname), duration=150)


def gif_wave(rs: float, varphi=PHI, outname="wave_packet.gif"):
    """
    Animate 1D wave packet propagation with c(x) = sqrt(A(r)).
    Shows wave propagation speed varying with spacetime curvature.
    """
    # Spatial grid
    x_min, x_max = 1.05*rs, 20*rs
    N_points = 500
    x = np.linspace(x_min, x_max, N_points)
    dx = x[1] - x[0]
    
    # Get A(x) for wave speed
    Asafe, rstar = A_safe(x, rs, varphi=varphi)
    c_local = np.sqrt(np.maximum(Asafe, 0.01))  # Local speed of light
    
    # Initial Gaussian wave packet
    x0 = 10 * rs
    sigma = 2 * rs
    k0 = 2 * np.pi / rs  # Wave number
    
    # Complex wave function
    psi_init = np.exp(-((x - x0)**2) / (2*sigma**2)) * np.exp(1j * k0 * x)
    
    frames = []
    
    # Time evolution (simplified advection)
    dt = 0.5
    t_max = 30
    
    psi = psi_init.copy()
    
    for t in np.arange(0, t_max, dt):
        # Simple advection: ∂ψ/∂t = -c(x) ∂ψ/∂x
        # Using upwind scheme
        psi_new = psi.copy()
        for i in range(1, N_points-1):
            dpsi_dx = (psi[i+1] - psi[i-1]) / (2*dx)
            psi_new[i] = psi[i] - dt * c_local[i] * dpsi_dx
        
        psi = psi_new
        
        # Every few steps, save a frame
        if int(t/dt) % 2 == 0:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), dpi=120, sharex=True)
            
            # Top: Wave packet amplitude
            ax1.plot(x/rs, np.abs(psi)**2, lw=2, color='blue')
            ax1.axvline(rstar/rs, ls=':', color='red', alpha=0.6, label='$r^*$')
            ax1.set(ylabel='$|\\psi|^2$', ylim=(0, 1.1),
                    title=f"Wave Packet — t = {t:.1f}")
            ax1.grid(alpha=0.3)
            ax1.legend()
            
            # Bottom: Local speed of light
            ax2.plot(x/rs, c_local, lw=2, color='green')
            ax2.axvline(rstar/rs, ls=':', color='red', alpha=0.6)
            ax2.set(xlabel='r/$r_s$', ylabel='$c_{local}/c$', ylim=(0, 1.1))
            ax2.grid(alpha=0.3)
            
            buf = io.BytesIO()
            plt.tight_layout()
            fig.savefig(buf, format="png")
            plt.close(fig)
            buf.seek(0)
            frames.append(Image.open(buf).convert("P"))
    
    _save_gif(frames, os.path.join(OUTDIR, outname), duration=100)


def main():
    """CLI entry point."""
    ap = argparse.ArgumentParser(
        description="SSZ Metric Visualization CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m viz_ssz_metric.sszviz_cli check --varphis 1.0 1.61803398875
  python -m viz_ssz_metric.sszviz_cli gif --kind all --varphi 1.0
  python -m viz_ssz_metric.sszviz_cli gif --kind time --varphi 1.61803398875
        """
    )
    
    ap.add_argument("--rs", type=float, default=1.0, 
                    help="Schwarzschild radius in chosen units (default: 1.0)")
    
    sub = ap.add_subparsers(dest="cmd", required=True, help="Subcommands")
    
    # Check command
    pchk = sub.add_parser("check", help="Check intersection points")
    pchk.add_argument("--varphis", type=float, nargs="+", 
                      default=[1.0, PHI],
                      help="List of φ values to check")
    
    # GIF command
    pgif = sub.add_parser("gif", help="Generate animated GIFs")
    pgif.add_argument("--kind", 
                      choices=["time", "A", "K", "lens", "wave", "all"], 
                      default="all",
                      help="Which GIF(s) to generate")
    pgif.add_argument("--varphi", type=float, default=PHI,
                      help=f"φ-parameter (default: {PHI:.10f})")
    
    args = ap.parse_args()
    
    if args.cmd == "check":
        cmd_check(args.rs, args.varphis)
    
    elif args.cmd == "gif":
        print(f"\n🎬 Generating GIF(s) with φ = {args.varphi:.6f}, r_s = {args.rs}\n")
        
        if args.kind in ("time", "all"):
            print("📊 Creating time dilation animation...")
            gif_time_dilation(args.rs, args.varphi)
        
        if args.kind in ("A", "all"):
            print("📊 Creating A(r) comparison animation...")
            gif_A_compare(args.rs, args.varphi)
        
        if args.kind in ("K", "all"):
            print("📊 Creating curvature proxy animation...")
            gif_curvature_proxy(args.rs, args.varphi)
        
        if args.kind in ("lens", "all"):
            print("📊 Creating gravitational lensing animation...")
            gif_lens(args.rs, args.varphi)
        
        if args.kind in ("wave", "all"):
            print("📊 Creating wave packet animation...")
            gif_wave(args.rs, args.varphi)
        
        print(f"\n✅ Done! Check: {OUTDIR}/\n")


if __name__ == "__main__":
    main()
