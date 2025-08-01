MODE_STYLER_CONFIG = {
    "default": {
        "background_class": "bg-white",
        "text_class": "text-gray-800",
        "button_class": "btn-outline-secondary",
    },
    "mystical": {
        "background_class": "bg-purple-100",
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
            'fact_container': 'bg-blue-100 rounded-lg p-4 border-l-4 border-blue-300',
            'title': 'font-medium text-blue-800',
            'text': 'text-sm text-blue-700',
            'subtitle': 'text-xs text-blue-600 mt-2',
            'fact_title': 'text-sm font-medium text-blue-900 mb-1'
        },
    }
    return styles.get(mode, styles.get('default', styles['mystical']))

def get_card_styles(mode):
    # Another helper for different component types
    pass