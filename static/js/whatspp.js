document.addEventListener('DOMContentLoaded', function () {
    // List of 50 popular languages (can be obtained from an external source)
    var languages = [
        'English', 'Spanish', 'French', 'German', 'Chinese', 'Japanese', 'Italian', 'Portuguese', 'Russian', 'Arabic',
        'Hindi', 'Bengali', 'Urdu', 'Turkish', 'Indonesian', 'Dutch', 'Polish', 'Thai', 'Vietnamese', 'Korean',
        'Persian', 'Malay', 'Swedish', 'Greek', 'Romanian', 'Hungarian', 'Czech', 'Danish', 'Finnish', 'Norwegian',
        'Hebrew', 'Swahili', 'Slovak', 'Bulgarian', 'Croatian', 'Serbian', 'Ukrainian', 'Lithuanian', 'Latvian',
        'Estonian', 'Slovenian', 'Icelandic', 'Maltese', 'Albanian', 'Macedonian', 'Georgian', 'Belarusian', 'Basque'
    ];

    // Sort languages alphabetically (ascending order)
    languages.sort();

    var selectLanguage = document.getElementById('language');

    // Add options to the dropdown menu
    languages.forEach(function (language) {
        var option = document.createElement('option');
        option.text = language;
        option.value = language.toLowerCase(); // Lowercase value for form submission
        selectLanguage.add(option);
    });
});