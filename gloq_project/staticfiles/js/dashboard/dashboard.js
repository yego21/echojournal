document.addEventListener('DOMContentLoaded', function() {
    // Modal functionality
    const entryModal = document.getElementById('entry-modal');
    const floatingNewDrop = document.getElementById('floating-new-drop');
    const closeEntryModal = document.getElementById('close-entry-modal');
    
    // Three-dot menu functionality
    const toolsToggle = document.getElementById('tools-toggle');
    const toolsDropdown = document.getElementById('tools-dropdown');
    
    // Toggle tools dropdown
    toolsToggle.addEventListener('click', function(e) {
        e.stopPropagation();
        toolsDropdown.classList.toggle('active');
    });
    
    // Close tools dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (toolsDropdown.classList.contains('active') && 
            !toolsDropdown.contains(e.target) && 
            !toolsToggle.contains(e.target)) {
            toolsDropdown.classList.remove('active');
        }
    });
    
    // Entry Modal - triggered by floating button
    floatingNewDrop.addEventListener('click', function() {
        // Clear any previous alerts
        const alertContainer = document.getElementById('form-alerts');
        if (alertContainer) {
            alertContainer.innerHTML = '';
        }
        
        entryModal.classList.add('active');
        
        // Focus on textarea when opened
        setTimeout(() => {
            const textarea = entryModal.querySelector('textarea');
            if (textarea) textarea.focus();
        }, 300);
    });

    closeEntryModal.addEventListener('click', function() {
        entryModal.classList.remove('active');
        // Clear form
        const form = document.getElementById('journal-form');
        if (form) form.reset();
    });

    // Close modals on overlay click
    entryModal.addEventListener('click', function(e) {
        if (e.target === entryModal) {
            entryModal.classList.remove('active');
            const form = document.getElementById('journal-form');
            if (form) form.reset();
        }
    });

    // Close modals on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            entryModal.classList.remove('active');
            toolsDropdown.classList.remove('active');
        }
    });
});

// Handle HTMX form submission responses
document.body.addEventListener('htmx:afterRequest', function(event) {
    console.log('HTMX afterRequest triggered', event.detail);
    
    if (event.detail.target && event.detail.target.id === 'journal-form') {
        const xhr = event.detail.xhr;
        const alertContainer = document.getElementById('form-alerts');
        const entryModal = document.getElementById('entry-modal');
        
        console.log('Form submission detected. Status:', xhr.status);
        console.log('Response text:', xhr.responseText);
        
        if (!alertContainer) {
            console.error('Alert container not found!');
            return;
        }
        
        try {
            const response = JSON.parse(xhr.responseText);
            console.log('Parsed response:', response);
            
            if (xhr.status === 200 && response.success) {
                console.log('Success case triggered');
                // Success - show message, reset and hide form
                alertContainer.innerHTML = `
                    <div class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg mb-4 fade-in">
                        ${response.message}
                    </div>
                `;
                
                // Reset form and close modal
                const form = document.getElementById('journal-form');
                if (form) form.reset();
                if (entryModal) entryModal.classList.remove('active');
                
                // Refresh stream content after new entry
                const streamContent = document.getElementById('stream-content');
                if (streamContent) {
                    htmx.ajax('GET', '{% url "journal:stream_content" %}', {
                        target: '#stream-content',
                        swap: 'innerHTML'
                    });
                }
                
                // Auto-hide success message after 5 seconds
                setTimeout(() => {
                    if (alertContainer) alertContainer.innerHTML = '';
                }, 5000);
                
            } else {
                console.log('Error case triggered');
                // Error - show error message
                alertContainer.innerHTML = `
                    <div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4 fade-in">
                        ${response.error || 'An unexpected error occurred.'}
                    </div>
                `;
            }
        } catch (e) {
            console.error('Error parsing response:', e);
            alertContainer.innerHTML = `
                <div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4 fade-in">
                    An error occurred while saving your entry.
                </div>
            `;
        }
    }
});

// Function to toggle AI Insights (now called Refractions)
let showingInsights = false;
let cachedModeFeaturesHTML = null;

function toggleAIInsights() {
    const contentTitle = document.getElementById('content-title');
    const dynamicContent = document.getElementById('dynamic-content');  
    const refractionsContainer = document.getElementById('refractions-content-container');
    const refractionsContent = document.getElementById('refractions-content');
    const button = document.getElementById('refraction-toggle');

    if (!cachedModeFeaturesHTML) {
        const modeFeatures = document.getElementById('mode-features');
        if (modeFeatures) {
            cachedModeFeaturesHTML = modeFeatures.innerHTML;
        } else {
            console.warn("mode-features not found in DOM.");
        }
    }

    if (showingInsights) {
        // Hide refractions
        contentTitle.textContent = 'Active Mode';        
        dynamicContent.innerHTML = '<div id="mode-features">' + cachedModeFeaturesHTML + '</div>';
        button.innerHTML = '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg><span>Refraction</span>';
        
        showingInsights = false;
        console.log("Switched back to Mode Features");
    } else {
        // Show refractions
        contentTitle.textContent = 'Refractions';
        button.innerHTML = '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg><span>Close</span>';
        
        // Load AI Insights in main content area
        htmx.ajax('GET', '{% url "journal:load_insight_panel" %}', {
            target: '#dynamic-content',
            swap: 'innerHTML'
        });
        
        showingInsights = true;
        console.log("Switched to AI Insights (Refractions)");
    }
}

// Theme & Panel Reload - Django functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('=== INITIAL MODE LOADING ===');
    console.log('Raw active_mode value:', '{{ active_mode }}');
    console.log('Raw background_class:', '{{ mode_styler.background_class }}');
    
    // 1. Load initial mode features via HTMX
    const initialModeSlug = '{{ active_mode }}';  // Using active_mode instead of active_mode.slug
    if (initialModeSlug) {
        console.log('Loading initial mode features for:', initialModeSlug);
        htmx.ajax('POST', '{% url "journal:_mode_features" %}', {
            values: { slug: initialModeSlug },
            target: '#mode-features',
            swap: 'innerHTML'
        });
    } else {
        console.log('WARNING: No initial mode slug found');
    }

    // 2. Apply initial background styling
    const initialBackgroundClass = '{{ mode_styler.background_class }}';
    const container = document.getElementById('journal_container');
    console.log('Container found:', container);
    console.log('Applying initial background class:', initialBackgroundClass);
    
    if (container && initialBackgroundClass) {
        // Remove any existing bg classes and apply initial one
        container.className = container.className.replace(/bg-\w+-\d+/g, '') + ' ' + initialBackgroundClass + ' min-h-screen transition-all duration-300';
        console.log('Final container classes:', container.className);
    }

    // 3. Load initial stream content
    const streamContent = document.getElementById('stream-content');
    if (streamContent) {
        htmx.ajax('GET', '{% url "journal:stream_content" %}', {
            target: '#stream-content',
            swap: 'innerHTML'
        });
    }

    console.log('=== INITIAL MODE LOADING COMPLETE ===');

    // 4. Set up event listener for dropdown changes
    document.body.addEventListener('updateTheme', function(event) {
        console.log('=== DROPDOWN CHANGE EVENT ===');
        console.log('updateTheme event fired:', event.detail);
        const { mode_slug, background_class } = event.detail;

        // Update container styling
        const container = document.getElementById('journal_container');
        console.log('Updating container with:', background_class);
        if (container) {
            container.className = container.className.replace(/bg-\w+-\d+/g, '') + ' ' + background_class + ' min-h-screen transition-all duration-300';
            console.log('Updated container classes:', container.className);
        }
        
        // Load new mode features
        console.log('Loading new mode features for:', mode_slug);
        htmx.ajax('POST', '{% url "journal:_mode_features" %}', {
            values: { slug: mode_slug },
            target: '#mode-features',
            swap: 'innerHTML'
        }); 
        console.log('=== DROPDOWN CHANGE COMPLETE ===');
    });
});
