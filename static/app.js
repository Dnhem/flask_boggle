// Global variables
let currentScore = 0;
let valid = false;
let counter = 60;
let words = new Set();

// 60 sec countdown function
const timer = setInterval(async function() {
  counter--;

  if (counter <= 0) {
    clearInterval(timer);
    $(".counter").html("<h3>Time's Up!</h3>");
    await postScore();
    return;
  } else {
    $(".counter").text(counter);
  }
}, 1000);

// Display guess results
const showResult = result => {
  let showResult;
  if (result === "ok") {
    showResult = "✅ Valid.";
    valid = true;
  } else if (result === "not-on-board") {
    showResult = "❌ Word not on grid.";
    valid = false;
  } else {
    showResult = "❗️ Not a word.";
    valid = false;
  }
  return `
  <li>${showResult}</li>
  `;
};

// Append score on page to display to user
const displayScore = score => {
  $(".currentScore").text(score);
};

// Check for duplicate words
const checkDuplicates = word => {
  if (!words.has(word)) {
    words.add(word);
    currentScore += word.length;
    displayScore(currentScore);
  } else {
    alert("You cannot use the same answer twice!");
  }
};

// Word form submission
$(".add-word").on("submit", async function(e) {
  e.preventDefault();
  const word = $(".word").val();
  const resp = await axios.get("/check-word", { params: { word: word } });
  const result = showResult(resp.data.result);
  $(".add-word").trigger("reset");
  $(".result").append(result);

  // add word to set & accumulate score (word length) if word is valid
  if (valid) {
    checkDuplicates(word);
  }
});

// Submit score to server
async function postScore() {
  $(".add-word").hide();
  $(".timer").hide();
  const resp = await axios.post("/post-score", { score: currentScore });
  console.log(resp);
}
