const userId = document.body.dataset.userId;
console.log(userId)
const questionOutput = document.getElementById("question-output");
const submitButton = document.getElementById("submit-code");
const editor = CodeMirror.fromTextArea(document.getElementById("code-editor"), {
    lineNumbers: true,
    mode: "python",
    theme: "default"
});

let currentQuestionId = null;
let currentQuestionText = null;
let currentConcept = null;

function fetchNextQuestion() {
    fetch("/get_next_question", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId })
    })
        .then(res => res.json())
        .then(data => {
            console.log(data)
            if (data.question_text) {
                currentQuestionId = data.question_id;
                currentQuestionText = data.question_text;
                currentConcept = data.concept;
                questionOutput.textContent = data.question_text;
            } else {
                questionOutput.textContent = "🎉 All questions completed!";
                submitButton.disabled = true;
            }
        });
}

submitButton.addEventListener("click", () => {
    const userCode = editor.getValue();

    fetch("/submit_answer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            user_id: userId,
            question_id: currentQuestionId,
            question_text: currentQuestionText,
            concept: currentConcept,
            code: userCode
        })
    })
        .then(res => res.json())
        .then(data => {
            const feedbackEl = document.getElementById("submission-feedback");
            feedbackEl.innerHTML = `<p>💡 <strong>Score:</strong> ${data.score}</p><p><strong>Response:</strong> ${data.response}</p>`;
            const coinDisplay = document.getElementById('coins');
            coinDisplay.innerText = `💰 Coins: ${data.coins}`;
            fetchNextQuestion();
        });
});

window.onload = fetchNextQuestion;