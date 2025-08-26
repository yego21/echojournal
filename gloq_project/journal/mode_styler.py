MODE_STYLER_CONFIG = {
    "default": {
        "background_class": "bg-white",
        "text_class": "text-gray-800",
        "button_class": "btn-outline-secondary",
    },
    "mystical": {
        # "background_class": "bg-purple-100",
        "header_background_class": "bg-gradient-to-r from-purple-100 to-indigo-100",
        # "content_background_class": "bg-gradient-to-br from-purple-25 to-indigo-25",

        "card_class": "bg-white border-l-4 border-purple-400 shadow-lg shadow-purple-100/50",
        "card_header_class": "bg-gradient-to-r from-purple-50 to-indigo-50 border-b border-purple-200",
        "feature_card_class": "bg-gradient-to-br from-purple-50 to-white border border-purple-200",

        "text_class": "text-blue-900",
        "button_class": "bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded shadow",
        "synthesis_reflect_class": "bg-purple-50 hover:bg-purple-100 border border-purple-200",
        "synthesis_digest_class": "bg-indigo-50 hover:bg-indigo-100 border border-indigo-200",
    # ... etc
},
    "philosophical": {
        "background_class": "bg-pink-100",
        "text_class": "text-pink-900",
        "button_class": "bg-green-500 hover:bg-green-600 text-black py-2 px-4 rounded-lg",
        "view_entries_class": "bg-green-50 border-green-300",
        "view_entries_button": "bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-2 rounded"
    },
}

MODE_HEADER_CONFIG = {
    "mystical": {
        "icon": "✨",
        "icon_bg": "bg-gradient-to-br from-purple-500 to-indigo-600",
        "title": "Mystical Journey",
        "description": "Explore the mysterious and transcendent realms",
        "svg": """
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                  d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"/>
        """
    },
    "philosophical": {
        "icon": "🤔",
        "icon_bg": "bg-gradient-to-br from-blue-500 to-indigo-600",
        "title": "Philosophical Inquiry",
        "description": "Engage in deep thinking and fundamental questions",
        "svg": """
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                  d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
        """
    },
    "creative": {
        "icon": "🎨",
        "icon_bg": "bg-gradient-to-br from-pink-500 to-rose-600",
        "title": "Creative Expression",
        "description": "Unleash your artistic potential and innovative thinking",
        "svg": """
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                  d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v14a2 2 0 01-2 2h-4zM7 3V1M13 21a4 4 0 004-4V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v14a2 2 0 002 2h4zM17 3V1"/>
        """
    },
    "exploratory": {
        "icon": "🔍",
        "icon_bg": "bg-gradient-to-br from-cyan-500 to-blue-600",
        "title": "Exploratory Discovery",
        "description": "Discover new horizons and uncharted territories",
        "svg": """
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
        """
    },
    "medical": {
        "icon": "⚕️",
        "icon_bg": "bg-gradient-to-br from-green-500 to-emerald-600",
        "title": "Medical Insights",
        "description": "Focus on health, wellness, and medical knowledge",
        "svg": """
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                  d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
        """
    },
    "spiritual": {
        "icon": "🕯️",
        "icon_bg": "bg-gradient-to-br from-teal-500 to-cyan-600",
        "title": "Spiritual Connection",
        "description": "Connect with deeper meaning and inner wisdom",
        "svg": """
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                  d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z"/>
        """
    },
    "visionary": {
        "icon": "🔮",
        "icon_bg": "bg-gradient-to-br from-indigo-500 to-purple-600",
        "title": "Visionary Thinking",
        "description": "Envision future possibilities and breakthrough ideas",
        "svg": """
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                  d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                  d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
        """
    },
    "productive": {
        "icon": "⚡",
        "icon_bg": "bg-gradient-to-br from-yellow-500 to-orange-600",
        "title": "Productive Focus",
        "description": "Optimize efficiency and achieve your goals",
        "svg": """
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                  d="M13 10V3L4 14h7v7l9-11h-7z"/>
        """
    }
}



def get_feature_styles(mode):
    styles = {
        'mystical': {
            'astronomical_container': 'bg-purple-50 rounded-lg p-4 mb-4',
            'action_container': 'bg-purple-100 rounded-lg p-4 mb-4 border-l-4 border-purple-300',
            'fact_container': 'bg-purple-50 rounded-lg p-4',
            'title': 'font-medium text-purple-800',
            'text': 'text-sm text-purple-700',
            'subtitle': 'text-xs text-purple-600 mt-2',
            'fact_title': 'text-sm font-medium text-purple-900 mb-1'
        },
          'philosophical': {
            'question_container': 'bg-blue-50 rounded-lg p-4',
            'action_container': 'bg-blue-100 rounded-lg p-4 mb-4 border-l-4 border-green-300',
             'fact_container': 'bg-blue-50 rounded-lg p-4',
            'title': 'font-medium text-blue-800',
            'text': 'text-sm text-blue-700',
            'subtitle': 'text-xs text-blue-600 mt-2',
            'fact_title': 'text-sm font-medium text-blue-900 mb-1'
        },
        'medical': {
            'question_container': 'bg-green-50 rounded-lg p-4 mb-4',
            'action_container': 'bg-green-100 rounded-lg p-4 mb-4 border-l-4 border-green-300',
            'fact_container': 'bg-green-50 rounded-lg p-4',
            'title': 'font-medium text-green-800',
            'text': 'text-sm text-green-700',
            'subtitle': 'text-xs text-green-600 mt-2',
            'fact_title': 'text-sm font-medium text-green-900 mb-1'
        },
        'creative': {
            'question_container': 'bg-pink-50 rounded-lg p-4 mb-4',
            'action_container': 'bg-pink-100 rounded-lg p-4 mb-4 border-l-4 border-pink-300',
            'fact_container': 'bg-pink-50 rounded-lg p-4',
            'title': 'font-medium text-pink-800',
            'text': 'text-sm text-pink-700',
            'subtitle': 'text-xs text-pink-600 mt-2',
            'fact_title': 'text-sm font-medium text-pink-900 mb-1'
        },
        'productive': {
            'question_container': 'bg-yellow-50 rounded-lg p-4 mb-4',
            'action_container': 'bg-yellow-100 rounded-lg p-4 mb-4 border-l-4 border-yellow-300',
            'fact_container': 'bg-yellow-50 rounded-lg p-4',
            'title': 'font-medium text-yellow-800',
            'text': 'text-sm text-yellow-700',
            'subtitle': 'text-xs text-yellow-600 mt-2',
            'fact_title': 'text-sm font-medium text-yellow-900 mb-1'
        },
        'exploratory': {
            'question_container': 'bg-cyan-50 rounded-lg p-4 mb-4',
            'action_container': 'bg-cyan-100 rounded-lg p-4 mb-4 border-l-4 border-cyan-300',
            'fact_container': 'bg-cyan-50 rounded-lg p-4',
            'title': 'font-medium text-cyan-800',
            'text': 'text-sm text-cyan-700',
            'subtitle': 'text-xs text-cyan-600 mt-2',
            'fact_title': 'text-sm font-medium text-cyan-900 mb-1'
        },
        'visionary': {
            'question_container': 'bg-indigo-50 rounded-lg p-4 mb-4',
            'action_container': 'bg-indigo-100 rounded-lg p-4 mb-4 border-l-4 border-indigo-300',
            'fact_container': 'bg-indigo-50 rounded-lg p-4',
            'title': 'font-medium text-indigo-800',
            'text': 'text-sm text-indigo-700',
            'subtitle': 'text-xs text-indigo-600 mt-2',
            'fact_title': 'text-sm font-medium text-indigo-900 mb-1'
        },
        'spiritual': {
            'question_container': 'bg-teal-50 rounded-lg p-4 mb-4',
            'action_container': 'bg-teal-100 rounded-lg p-4 mb-4 border-l-4 border-teal-300',
            'fact_container': 'bg-teal-50 rounded-lg p-4',
            'title': 'font-medium text-teal-800',
            'text': 'text-sm text-teal-700',
            'subtitle': 'text-xs text-teal-600 mt-2',
            'fact_title': 'text-sm font-medium text-teal-900 mb-1'
        }
    }
    return styles.get(mode, styles.get('default', styles['mystical']))

def get_card_styles(mode):
    # Another helper for different component types
    pass