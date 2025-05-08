let errorEditor = CodeMirror.fromTextArea(document.getElementById("error-code-editor"), {
    mode: "python",
    theme: "default",
    lineNumbers: true,
    readOnly: true,
    tabSize: 4,
    indentUnit: 4,
    viewportMargin: Infinity
});

let userEditor = CodeMirror.fromTextArea(document.getElementById("user-code-editor"), {
    mode: "python",
    theme: "default",
    lineNumbers: true
});

async function loadCode(difficulty) {
    const response = await fetch("/get_code", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ difficulty })
    });
    const data = await response.json();

    if (data.error) {
        errorEditor.setValue(data.error);
    } else if (data.code) {
        const match = data.code.match(/```(?:python)?\s*([\s\S]*?)```/i);
        const rawCode = match ? match[1].trim() : data.code.trim();
        errorEditor.setValue(rawCode);

        const lineCount = errorEditor.lineCount();
        const lineHeight = 20;
        errorEditor.setSize(null, `${lineCount * lineHeight + 10}px`);
    } else {
        errorEditor.setValue("No error code");
    }
    userEditor.setValue("");
    document.getElementById("result-display").textContent = "";
}

document.getElementById("submit-btn").addEventListener("click", async () => {
    const errorCode = errorEditor.getValue();
    const userCode = userEditor.getValue();

    const response = await fetch("/check_solution", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ error_code: errorCode, user_code: userCode })
    });

    const result = await response.json();
    document.getElementById("result-display").textContent = result.result;
});
