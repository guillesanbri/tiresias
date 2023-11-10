# TiresIAs

TL;DR: I’ve stiched a few APIs together to ask GPT4 questions about whatever happens to be in front of you, potentially useful for visually impaired people.

Devlog/blogpost/whatever you wanna call it about the project [here (TBA)]().

### Demo video

![Video placeholder](https://images.placeholders.dev/?width=720&height=256&text=Video%20placeholder)

---

Currently this repo only holds a quite simple proof-of-concept, the inner working is outlined in the diagram below. Basically, the `run` function takes an audio file with a question and an image, (1) converts the audio to text using Whisper, (2) asks GPT-4V the corresponding question while passing the context image, and then it (3) converts the answer to the question to audio using GCP Text-to-Speech API.

![Workflow of the initial proof of concept for TiresIAs.](drawio/poc_flow.png)

---

# Instructions to install/run the project
Soon™️

---

# Backlog
Main things I want to add in the near future listed in no particular order.

[ ] Add demo video
[ ] Add instructions to the readme + requirements and so on.
[ ] Add speech thresholding / question extraction before S2T.
[ ] Local whisper (whisper.cpp).
[ ] Local Vision-Language model (BakLLaVA?).
[ ] Android app (API-based).
[ ] Android app (on-device models).
[ ] Jetson edge execution + glasses.

---