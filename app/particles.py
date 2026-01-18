"""
Floating particles background effect for the app.
"""
import random


def render_particles(particles_config=None):
    """
    Returns HTML/CSS for animated floating particles that react to mouse hover.
    Particles are varied in brightness and move away when hovered.
    Positions are randomized only once and can be reused across reruns.

    Args:
        particles_config: Optional pre-generated particles configuration to maintain consistency

    Returns:
        tuple: (html_string, particles_config) for reuse in session state
    """
    # Generate random positions for particles only if not provided
    if particles_config is None:
        particles = []
        # Create particles distributed across the screen
        for i in range(35):  # Increased particle count for better coverage
            size = random.randint(6, 12)
            # Ensure better distribution by splitting into grid zones
            if i < 18:
                # First half - spread across full width
                left = random.randint(1, 98)
            else:
                # Second half - ensure left side coverage
                left = random.randint(1, 50)
            top = random.randint(1, 98)
            anim = random.choice(
                ["float", "float-reverse", "float-slow"]
            )  # Removed twinkle - all particles move
            duration = random.randint(8, 15)
            delay = random.uniform(0, 3)
            # Some particles are brighter (clearer) than others
            brightness = random.choice(["dim", "medium", "bright"])
            # Random direction for hover movement - restricted to 30-70px
            move_x = random.choice([-1, 1]) * random.randint(30, 70)
            move_y = random.choice([-1, 1]) * random.randint(30, 70)
            particles.append(
                {
                    "id": i + 1,
                    "size": size,
                    "top": top,
                    "left": left,
                    "anim": anim,
                    "duration": duration,
                    "delay": delay,
                    "brightness": brightness,
                    "move_x": move_x,
                    "move_y": move_y,
                }
            )
    else:
        particles = particles_config

    # Build particle CSS and HTML
    particle_styles = []
    particle_divs = []

    for p in particles:
        # Adjust opacity based on brightness
        opacity_base = {"dim": 0.35, "medium": 0.6, "bright": 0.85}[p["brightness"]]
        opacity_peak = {"dim": 0.55, "medium": 0.8, "bright": 1.0}[p["brightness"]]

        particle_styles.append(
            f".particle-wrapper-{p['id']} {{ "
            f"top: {p['top']}%; left: {p['left']}%; "
            f"animation: {p['anim']} {p['duration']}s ease-in-out infinite {p['delay']}s; "
            f"--opacity-base: {opacity_base}; --opacity-peak: {opacity_peak}; "
            f"}} "
            f".particle-inner-{p['id']} {{ "
            f"width: {p['size']}px; height: {p['size']}px; "
            f"}} "
            f".particle-wrapper-{p['id']}:hover .particle-inner-{p['id']} {{ "
            f"transform: translate({p['move_x']}px, {p['move_y']}px) scale(2.5) !important; "
            f"}}"
        )
        particle_divs.append(
            f'<div class="particle-wrapper particle-wrapper-{p["id"]}"><div class="particle-inner particle-inner-{p["id"]}"></div></div>'
        )

    styles_str = "\n        ".join(particle_styles)
    divs_str = "\n        ".join(particle_divs)

    return (
        f"""
        <style>
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px) translateX(0px); opacity: var(--opacity-base); }}
            50% {{ transform: translateY(-25px) translateX(12px); opacity: var(--opacity-peak); }}
        }}
        @keyframes float-reverse {{
            0%, 100% {{ transform: translateY(0px) translateX(0px); opacity: var(--opacity-base); }}
            50% {{ transform: translateY(25px) translateX(-12px); opacity: var(--opacity-peak); }}
        }}
        @keyframes float-slow {{
            0%, 100% {{ transform: translateY(0px) translateX(0px) rotate(0deg); opacity: var(--opacity-base); }}
            50% {{ transform: translateY(-18px) translateX(-10px) rotate(180deg); opacity: var(--opacity-peak); }}
        }}
        .particle-wrapper {{
            position: fixed;
            z-index: 0;
            pointer-events: auto;
            padding: 25px;
            cursor: default;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .particle-inner {{
            background: radial-gradient(circle, rgba(76, 210, 240, 0.95) 0%, rgba(76, 210, 240, 0.5) 40%, transparent 70%);
            border-radius: 50%;
            pointer-events: none;
            transition: all 0.2s ease-out;
            filter: blur(0.5px);
            box-shadow: 0 0 8px rgba(76, 210, 240, 0.6);
        }}
        .particle-wrapper:hover .particle-inner {{
            background: radial-gradient(circle, rgba(255, 20, 147, 0.95) 0%, rgba(123, 104, 238, 0.7) 40%, rgba(76, 210, 240, 0.4) 70%, transparent 90%);
            filter: blur(1px);
            box-shadow: 0 0 20px rgba(255, 20, 147, 0.8), 0 0 40px rgba(123, 104, 238, 0.5);
        }}
        {styles_str}
        </style>
        {divs_str}
    """,
        particles,
    )
