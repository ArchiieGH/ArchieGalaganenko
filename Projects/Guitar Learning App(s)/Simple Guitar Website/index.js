
const noteLabel = document.getElementById("noteLabel")
const btnGenerateNote = document.getElementById("btnGenerateNote");
const cbNaturalNotes = document.getElementById("cbNaturalNotes");
const cbAccidentalNotes = document.getElementById("cbAccidentalNotes");
const bpmLabel = document.getElementById("bpmLabel");
const bpmRange = document.getElementById("bpmRange");
const cbMetronome = document.getElementById("cbMetronome");

btnGenerateNote.addEventListener("click", () => {

    const naturalNotes = ["C", "D", "E", "F", "G", "A", "B"];
    const accidentalNotes = ["C#/Db", "D#/Eb", "F#/Gb", "G#/Ab", "A#/Bb"];

    let noteArray = [];
    if (cbNaturalNotes.checked == true){
        noteArray = noteArray.concat(naturalNotes);
    }
    if (cbAccidentalNotes.checked == true){
        noteArray = noteArray.concat(accidentalNotes);
    }
    noteLabel.textContent = noteArray[Math.floor(Math.random() * noteArray.length) + 0]
    click.currentTime = 0;
    click.play();

});

const audioContext = new (window.AudioContext)();
const click = "click_1.mp3";
let audioBuffer;

fetch(click)
    .then(response => response.arrayBuffer())
    .then(data => audioContext.decodeAudioData(data))
    .then(buffer => {
        audioBuffer = buffer;
    });

let isPlaying = false;
let nextNoteTime = 0;
let bpm = 100;
let interval = 60 / bpm;

function scheduleSound(time) {
    const source = audioContext.createBufferSource();
    source.buffer = audioBuffer;
    source.connect(audioContext.destination);
    source.start(time);
}

function startMetronome() {
    isPlaying = true;
    nextNoteTime = audioContext.currentTime;
    scheduleNextBeat();
}

function scheduleNextBeat() {
    if (!isPlaying) return;

    const now = audioContext.currentTime;

    if (nextNoteTime < now + 0.1) {
        scheduleSound(nextNoteTime);
        nextNoteTime += interval;
    }

    setTimeout(scheduleNextBeat, 25);
}

function stopMetronome() {
    isPlaying = false;
}

cbMetronome.addEventListener("change", () => {

    if (cbMetronome.checked) {
        startMetronome();
        } else {
          stopMetronome();
    }
});

bpmRange.addEventListener('input', () => {

    bpm = parseInt(bpmRange.value, 10);
    interval = 60 / bpm;
    bpmLabel.textContent = bpmRange.value;
});




