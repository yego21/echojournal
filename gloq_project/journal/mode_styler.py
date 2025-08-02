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