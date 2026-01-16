"""
SVG Icon Manager Module

Simple, lightweight SVG icon manager with lazy loading.


Usage in Templates:
-------------------
The icon() function is available in all Jinja2 templates:

    {{ icon('plus') }}                                    # Basic icon
    {{ icon('edit', 'btn-icon') }}                        # Icon with CSS class
    {{ icon('search', 'icon-lg', width=32, height=32) }}  # Icon with custom size
    {{ icon('user', aria_label='User profile') }}         # Icon with accessibility


Error Handling:
---------------
- Missing icon files: Renders fallback question mark icon, logs warning
- Invalid SVG files: Skipped during load, fallback rendered when requested
- Missing icons directory: Raises FileNotFoundError during initialization
- All errors are logged for debugging
"""

from typing import Optional
import re
from pathlib import Path
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)


class IconManager:
    """
    Simple, lightweight SVG icon manager with lazy loading.
    
    Attributes:
    -----------
    icons_dir : Path
        Path to the directory containing SVG icon files
    icons : dict[str, str]
        Cache of loaded icon SVG content (icon_name -> svg_content)
    
    Methods:
    --------
    render(name, css_class='', **kwargs) -> str
        Render an icon with optional customizations
    
    Example:
    --------
        >>> manager = IconManager(icons_dir='web/icons')
        >>> svg = manager.render('plus', 'btn-icon')
        >>> print(svg)
        <svg class="btn-icon icon icon-tabler..." width="24" height="24">...</svg>
    
    Notes:
    ------
    - Icon filenames use hyphens (e.g., chevron-left.svg)
    - In code, use underscores (e.g., icon('chevron_left'))
    - Manager automatically converts underscores to hyphens
    """
    
    def __init__(self, icons_dir: str = "web/icons"):
        """
        Initialize the Icon Manager.
        
        Sets up the icon manager with the specified icons directory. The directory
        must exist or a FileNotFoundError will be raised. No icons are loaded at
        initialization - they are loaded on-demand when first requested.
        
        Args:
            icons_dir: Path to the icons directory (default: 'web/icons')
                      Can be absolute or relative to the application root.
        
        Raises:
            FileNotFoundError: If the icons directory does not exist
        
        Example:
            >>> manager = IconManager()  # Uses default 'web/icons'
            >>> manager = IconManager(icons_dir='custom/icons')  # Custom directory
        
        Notes:
            - Directory must exist before initialization
            - No icons are loaded at initialization (lazy loading)
            - Logs initialization success with directory path
        """
        self.icons_dir = Path(icons_dir)
        self.icons: dict[str, str] = {}
        
        # Verify icons directory exists
        if not self.icons_dir.exists():
            logger.error(f"Icons directory not found: {self.icons_dir}")
            raise FileNotFoundError(f"Icons directory not found: {self.icons_dir}")
        
        logger.info("Icon manager initialized (lazy loading enabled)")
    
    def _load_icon(self, name: str) -> Optional[str]:
        """
        Load an icon from disk.
        
        Reads the SVG file from the icons directory and validates it. The icon name
        is converted from underscores to hyphens for the filename lookup.
        
        Args:
            name: Icon name with underscores (e.g., 'chevron_left', 'plus')
                 Will be converted to hyphenated filename (e.g., 'chevron-left.svg')
        
        Returns:
            SVG content as string if found and valid, None otherwise
        
        Example:
            >>> svg = manager._load_icon('chevron_left')
            >>> print(svg)
            <svg xmlns="http://www.w3.org/2000/svg"...>...</svg>
        
        Notes:
            - Converts underscores to hyphens for filename
            - Validates SVG content before returning
            - Logs warning if file not found or invalid
            - Returns None on any error (file not found, invalid SVG)
        """
        # Convert underscores to hyphens for filename
        filename = name.replace('_', '-') + '.svg'
        svg_file = self.icons_dir / filename
        
        if not svg_file.exists():
            logger.warning(f"Icon file not found: {svg_file}")
            return None
        
        # Read SVG content
        svg_content = svg_file.read_text(encoding='utf-8').strip()
        
        # Validate SVG
        if not self._is_valid_svg(svg_content):
            logger.warning(f"Invalid SVG file: {svg_file}")
            return None
        
        return svg_content
    
    def _is_valid_svg(self, svg: str) -> bool:
        """
        Validate that string contains valid SVG markup.
        
        Args:
            svg: SVG markup string
        
        Returns:
            True if valid, False otherwise
        """
        return '<svg' in svg and '</svg>' in svg
    
    @lru_cache(maxsize=512)
    def render(
        self,
        name: str,
        css_class: str = "",
        width: Optional[int] = None,
        height: Optional[int] = None,
        stroke_width: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        Render icon as HTML string with customizations.
        
        This is the main method for rendering icons. Icons are loaded on-demand and
        cached in memory. The rendered output is also cached using LRU cache for
        maximum performance.
        
        Args:
            name: Icon name (e.g., 'chevron_left', 'plus', 'edit')
                 Use underscores in code; they're converted to hyphens for file lookup
            css_class: Additional CSS classes to apply (default: '')
                      Added to existing classes in the SVG
            width: Custom width in pixels (default: None, uses SVG default)
                  Overrides the default width attribute
            height: Custom height in pixels (default: None, uses SVG default)
                   Overrides the default height attribute
            stroke_width: Custom stroke width (default: None, uses SVG default)
                         Overrides the default stroke-width attribute
            **kwargs: Additional SVG attributes as keyword arguments
                     Underscores in keys are converted to hyphens
                     Example: aria_label='Search' becomes aria-label="Search"
        
        Returns:
            Rendered SVG markup as string
            Returns fallback icon if the requested icon is not found or invalid
        
        Examples:
            Basic icon:
                >>> manager.render('plus')
                '<svg class="icon icon-tabler..." width="24" height="24">...</svg>'
            
            Icon with CSS class:
                >>> manager.render('edit', 'btn-icon')
                '<svg class="btn-icon icon icon-tabler..." width="24" height="24">...</svg>'
            
            Icon with custom size:
                >>> manager.render('search', 'icon-lg', width=32, height=32)
                '<svg class="icon-lg icon icon-tabler..." width="32" height="32">...</svg>'
            
            Icon with accessibility:
                >>> manager.render('user', aria_label='User profile')
                '<svg class="icon icon-tabler..." aria-label="User profile">...</svg>'
            
            Icon with multiple customizations:
                >>> manager.render('heart', 'favorite-icon', width=48, stroke_width=3, aria_label='Favorite')
                '<svg class="favorite-icon icon..." width="48" stroke-width="3" aria-label="Favorite">...</svg>'

        Error Handling:
            - Missing icon: Returns fallback question mark icon, logs warning
            - Invalid SVG: Returns fallback icon, logs warning
            - Fallback icon includes title attribute with missing icon name
        
        Notes:
            - Icon is loaded from disk on first request
            - Loaded SVG content is cached in self.icons dict
            - Rendered output is cached by @lru_cache decorator
            - Cache key includes all parameters (name, css_class, kwargs)
            - Different customizations create separate cache entries
        """
        # Get icon SVG (load if not cached)
        if name not in self.icons:
            svg = self._load_icon(name)
            if svg:
                self.icons[name] = svg
            else:
                logger.warning(f"Icon not found: {name}")
                return self._render_fallback(name, css_class)
        
        svg = self.icons[name]
        
        # Apply customizations
        if css_class:
            svg = self._add_css_class(svg, css_class)
        if width is not None:
            svg = self._set_attribute(svg, 'width', str(width))
        if height is not None:
            svg = self._set_attribute(svg, 'height', str(height))
        if stroke_width is not None:
            svg = self._set_attribute(svg, 'stroke-width', str(stroke_width))
        
        # Apply additional attributes
        for attr, value in kwargs.items():
            svg = self._set_attribute(svg, attr.replace('_', '-'), str(value))
        
        return svg
    
    def _add_css_class(self, svg: str, css_class: str) -> str:
        """
        Add CSS class to SVG element.
        
        Adds the specified CSS class to the SVG element's class attribute. If the
        SVG already has a class attribute, the new class is prepended. If not, a
        new class attribute is added.
        
        Args:
            svg: SVG markup string
            css_class: CSS class to add
        
        Returns:
            Modified SVG markup with added CSS class
        
        Example:
            >>> svg = '<svg class="icon" width="24">...</svg>'
            >>> result = manager._add_css_class(svg, 'btn-icon')
            >>> print(result)
            <svg class="btn-icon icon" width="24">...</svg>
        """
        if 'class="' in svg:
            svg = svg.replace('class="', f'class="{css_class} ', 1)
        else:
            svg = svg.replace('<svg ', f'<svg class="{css_class}" ', 1)
        return svg
    
    def _set_attribute(self, svg: str, attr: str, value: str) -> str:
        """
        Set or update SVG attribute.
        
        Sets or updates an attribute in the SVG element. If the attribute already
        exists, it's replaced with the new value. If not, it's added to the SVG tag.
        
        Args:
            svg: SVG markup string
            attr: Attribute name (e.g., 'width', 'height', 'aria-label')
            value: Attribute value
        
        Returns:
            Modified SVG markup with updated attribute
        
        Example:
            >>> svg = '<svg width="24" height="24">...</svg>'
            >>> result = manager._set_attribute(svg, 'width', '48')
            >>> print(result)
            <svg width="48" height="24">...</svg>
        
        Notes:
            - Uses regex to match attribute with space before it
            - Prevents matching partial attribute names (e.g., 'width' vs 'stroke-width')
            - If attribute doesn't exist, adds it to the opening <svg> tag
        """
        # Match attribute with space before it to avoid matching partial attribute names
        # e.g., 'width' should not match 'stroke-width'
        # Pattern matches: space + attribute + ="value"
        pattern = f'(\\s){re.escape(attr)}="[^"]*"'
        if re.search(pattern, svg):
            # Replace but keep the space
            svg = re.sub(pattern, f'\\1{attr}="{value}"', svg)
        else:
            svg = svg.replace('<svg ', f'<svg {attr}="{value}" ', 1)
        return svg
    
    def _render_fallback(self, name: str, css_class: str = "") -> str:
        """
        Render fallback icon for missing or invalid icons.
        
        Returns a question mark icon as a fallback when the requested icon cannot
        be found or is invalid. The fallback includes a title attribute showing
        which icon was not found.
        
        Args:
            name: Name of the missing icon
            css_class: CSS classes to apply to the fallback icon
        
        Returns:
            Fallback SVG markup (question mark icon)
        
        Example:
            >>> fallback = manager._render_fallback('nonexistent_icon', 'btn-icon')
            >>> print(fallback)
            <svg class="icon icon-tabler icon-tabler-question-mark btn-icon" 
                 title="Icon not found: nonexistent_icon">...</svg>
        
        Notes:
            - Always returns a valid SVG element
            - Includes title attribute for debugging
            - Uses Tabler Icons question mark icon
            - Preserves CSS classes from original request
        """
        fallback_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-question-mark {css_class}" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round" title="Icon not found: {name}"><path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M8 8a3.5 3 0 0 1 3.5 -3h1a3.5 3 0 0 1 3.5 3a3 3 0 0 1 -2 3a3 4 0 0 0 -2 4"></path><line x1="12" y1="19" x2="12" y2="19.01"></line></svg>'''
        return fallback_svg
