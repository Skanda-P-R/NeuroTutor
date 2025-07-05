const codeEditor = CodeMirror.fromTextArea(document.getElementById('code-editor'), {
    mode: 'python',
    theme: 'default',
    lineNumbers: true,
    indentUnit: 4,
    tabSize: 4,
    indentWithTabs: false,
    autoCloseBrackets: true,
    matchBrackets: true,
    lint: true
});

let currentErrors = [];

document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        tab.classList.add('active');
        const tabName = tab.getAttribute('data-tab');
        document.getElementById(`${tabName}-content`).classList.add('active');
    });
});

document.getElementById('check-errors').addEventListener('click', async () => {
    const code = codeEditor.getValue();

    const errorsOutput = document.getElementById('errors-output');
    const correctedOutput = document.getElementById('corrected-output');

    const errorSpinner = document.getElementById("error-spinner");
    const spinnerText = document.getElementById("spinner_text");

    const correctedSpinner = document.querySelector('#corrected-output .spinner');

    spinnerText.textContent = "Checking for errors...";
    spinnerText.style.display = "inline";
    errorSpinner.style.display = "inline-block";

    correctedOutput.textContent = 'Generating corrected code...';
    if (correctedSpinner) correctedSpinner.style.display = "inline-block";

    try {
        const response = await fetch('/check_errors', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code }),
        });

        const data = await response.json();
        const corrected_code = data.correct_code || [];
        const errors = data.errors_from_symbolic || [];

        if (errors.length === 0) {
            spinnerText.textContent = 'No errors found!';
            correctedOutput.textContent = 'No correction of code required...';
        } else {
            spinnerText.style.display = "none";
            errorSpinner.style.display = "none";

            errorsOutput.innerHTML = marked.parse(errors.join("\n"));
            correctedOutput.innerHTML = marked.parse(corrected_code.join("\n"));
        }

        document.querySelector('.tab[data-tab="errors"]').click();
    } catch (error) {
        spinnerText.textContent = `Error: ${error.message}`;
        correctedOutput.textContent = `Error: ${error.message}`;
    } finally {
        errorSpinner.style.display = "none";
        if (correctedSpinner) correctedSpinner.style.display = "none";
    }
});

document.getElementById('refresh-btn').addEventListener('click', function () {
        location.reload();
    });
