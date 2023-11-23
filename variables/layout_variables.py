
class GlobalLayouts():
    def _get_color_scheme():
        class ColorScheme():
            class Green():
                dark = "#008080"
                light = "#d9ecec"
                background = "#e9f0f0"
                
            class Purple():
                dark = "#4B2977"
                light = "#DFD9EC"
                background = "#ebe9f0"
                
            class Blue():
                dark = "#1A4B79"
                light = "#D9E2EC"
                background = "#ebf0f5"
                
            class Red():
                light = "#ECDDD9"
                dark = "#9E3838"
                background = "#f0eae9"

        scheme =  "Green"

        if scheme=="Green":
            dark = ColorScheme.Green.dark
            light = ColorScheme.Green.light
            background = ColorScheme.Green.background
        elif scheme=="Purple":
            dark = ColorScheme.Purple.dark 
            light = ColorScheme.Purple.light
            background = ColorScheme.Purple.background
        elif scheme=="Blue":
            dark = ColorScheme.Blue.dark 
            light = ColorScheme.Blue.light 
            background = ColorScheme.Blue.background
        elif scheme=="Red":
            dark = ColorScheme.Red.dark
            light = ColorScheme.Red.light 
            background = ColorScheme.Red.background
            
        return dark, light, background

    DARK_COLOR, LIGHT_COLOR, BACKGROUND_COLOR = _get_color_scheme()
    
    input_style = {
        "backgroundColor": BACKGROUND_COLOR,
    }
    
    container_style = {
        "margin": "5px 5px 5px 5px",
    }
    
    tab_style = {
        "fontWeight": "bold",
        "backgroundColor": LIGHT_COLOR, 
        "color": "black", 
        "font-size": "100%",
        "border-style": "ridge", 
        "border-style": "none",
        "margin": "15px",            
    }

    tab_selected_style = {
        "backgroundColor": DARK_COLOR,
        "color": "white", 
        "font-size": "100%", 
        "font-style": "oblique",
        "text-shadow": "10px 10px 10px gray", 
        "fontWeight": "900", 
        "margin": "15px",
    } 
    
    basic_font_style = {
        "font_family": "courier new",
        "font-size": "75%",
        "font-weight": "bold",
    }
    
    header_style = basic_font_style | {
        "backgroundColor": DARK_COLOR,
        "border-style": "none",
        "color": "white",
        "font-size": "32px",
        "font-style": "oblique",
        "font-weight": "bold",
        "margin": "0px 5px 0px 5px",
        "padding": "10px 0px 10px 0px",
        "text-shadow": "10px 10px 10px gray",
        "text-align": "center",
    }
    
    dropdown_style = {
        "backgroundColor": LIGHT_COLOR,
        "border-style": "none",
    }