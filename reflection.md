# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

---

it looked like it worked but the limit generation for diffulties felt off, the number was 69 but it kept prompting me to go higher
- the developer debug info section only updates during certain cases, and that was strange..
the developer debug section also did not update on my first attempt
- the attempts left section was not dynamic

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
i used claude to work on this

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

the difficulty was not being updated dymically and claude figured that it was not being stored in session state, and showed me evidence with lines were it was excluded. It suggested i add difficulty to session_state and that solved the issue..

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

there was no example of that

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

after fixing the difficulty state bug, changing to Easy actually changed the range and attempts. I ran pytest tests/ on the test file, which covers get_range_for_difficulty, check_guess, parse_guess, and update_score. The tests showed me that the Normal and Hard difficulty ranges were swapped in the original code  

Claude helped me understand what the tests were checking and how pytest output maps back to specific functions in the code.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

The original app called random.randint(low, high) at the top level every time the script ran, without any guard. In Streamlit, every button click or input triggers a full re-execution of the entire script, so a new random number got picked on every interaction with the app.
 
Streamlit is like a whiteboard that gets completely erased and redrawn every time you click anything. Any variable disappears but session state is like sticky notes you pin to the board and write on..

I wrapped the random.randint() call inside a condition that checks if a secret already exists in session state. So instead of generating a number every run, the code only generates one when there isn't one.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

  -I learned the importance of pausing and thinking before coding through this project.

- What is one thing you would do differently next time you work with AI on a coding task?
Claude can sound confident even when the fix is partial or introduces a new problem elsewhere. Next time I work with AI on a coding task, I would verify each suggestion against the actual code before applying it.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
  - 

  This project taught me that AI-generated code can look correct, and still have logic errors hiding in it
