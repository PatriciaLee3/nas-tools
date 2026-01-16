import logging
from markupsafe import Markup
from web.utils.icon_manager import IconManager

logger = logging.getLogger(__name__)


def register_icon_helper(app):
    """
    Register icon-related template globals with the Flask app.

    Args:
        app: The Flask application instance
    """
    # Initialize icon manager with configuration support
    icons_dir = app.config.get('ICONS_DIR', 'web/icons')
    
    try:
        icon_manager = IconManager(icons_dir=icons_dir)
        logger.info(f"Icon manager initialized successfully with directory: {icons_dir}")
    except FileNotFoundError as e:
        logger.error(f"Failed to initialize icon manager: {e}")
        # Create a fallback icon manager that will always return fallback icons
        icon_manager = None
    except Exception as e:
        logger.error(f"Unexpected error initializing icon manager: {e}")
        icon_manager = None

    @app.context_processor
    def inject_icon_function():
        """Make icon() function available in all templates."""
        def icon(name: str, css_class: str = '', **kwargs) -> Markup:
            """
            Render an icon in templates.
            
            Args:
                name: Icon name (e.g., 'plus', 'edit', 'search')
                css_class: Optional CSS classes to apply
                **kwargs: Additional SVG attributes (e.g., width=32, aria_label='Search')
            
            Returns:
                Rendered SVG markup as Markup object (safe for HTML rendering)
            
            Examples:
                {{ icon('plus') }} → Basic icon
                {{ icon('edit', 'btn-icon') }} → Icon with CSS class
                {{ icon('search', 'icon-lg', width=32, height=32) }} → Icon with custom size
                {{ icon('user', 'profile-icon', aria_label='User profile') }} → Icon with accessibility
            """
            if not name:
                return Markup('')
            
            # If icon manager failed to initialize, return a simple fallback
            if icon_manager is None:
                logger.warning(f"Icon manager not available, returning fallback for: {name}")
                return Markup(f'<svg xmlns="http://www.w3.org/2000/svg" class="icon {css_class}" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round" title="Icon system unavailable"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><circle cx="12" cy="12" r="9"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>')
            
            try:
                result = icon_manager.render(name, css_class, **kwargs)
                return Markup(result)
            except Exception as e:
                logger.error(f"Error rendering icon '{name}': {e}")
                return Markup(icon_manager._render_fallback(name, css_class))
        
        return {'icon': icon}
