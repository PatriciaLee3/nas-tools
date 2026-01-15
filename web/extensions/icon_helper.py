from flask import get_template_attribute


def register_icon_helper(app):
    """
    Register icon-related template globals with the Flask app.

    Args:
        app: The Flask application instance
    """

    @app.template_global('icon')
    def render_icon(icon_name: str, class_str: str = '') -> str:
        """
        Render an SVG icon by name using the SVG macro module.

        Args:
            icon_name: Name of the icon macro to call (e.g., 'home', 'movie')
            class_str: Optional CSS classes to pass to the macro

        Returns:
            Rendered HTML string of the icon, or empty string if icon not found

        Examples:
            {{ icon('home') }} → Renders the home icon
            {{ icon('movie', 'text-muted') }} → Renders the movie icon with custom class
        """
        if not icon_name:
            return ''
        try:
            # Get the SVG template module and call the macro
            svg_module = get_template_attribute('macro/svg.html', icon_name)
            return svg_module(class_str)
        except Exception:
            return ''
