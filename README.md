# Space Invaders Invader (Hackers of the Galaxy)

## Inspiration
For this hackathon, we were gunning (pun intended) for the “out of this world” theme, and decided to create a spin on the classic Space Invaders that you could play against your friends or an artificially intelligent agent. We wanted our project to showcase the power of deep reinforcement learning models in an interactive and visual way, while putting the player’s own intelligence (or maybe just common sense/trivia knowledge) to the test.

## What it does

In Space Invaders Invader, you as the human player pit your family feud knowledge against an AI agent (personified by Jessica Chastain, star of various outer space-themed movies) pre-trained to play Space Invaders! The more questions you answer correctly (and with higher score), the more you can mess with her expert actions by increasing the probability that she takes a random different action instead. When you successfully interfere with her actions, Jessica’s eyes light up red (better hope she’s not [Wanda](https://static2.cbrimages.com/wordpress/wp-content/uploads/2020/09/Scarlet-Witch-from-Endgame.jpg) in disguise!). Try your best to beat her in her home turf!

## How we built it

This program was built on pygame and OpenAI Gym’s [Atari Space Invaders environment](https://gym.openai.com/envs/SpaceInvaders-v0/). The Space Invaders agent was pre-trained courtesy of Uber Engineering's [Atari model zoo](https://github.com/uber-research/atari-model-zoo). The Family Feud component makes use of Python’s Levenshtein edit distance package.

## Challenges we ran into

Turns out, rendering both an Atari emulator and pygame visuals was super computationally demanding and caused a ton of lag on both ends (who'd have guessed?). As a result, we had to take a threaded approach, running Space Invaders in a separate thread and using a queue-based message-passing system for communication.

## Accomplishments that we're proud of

We’re incredibly proud of both the existing and newly learned skills we were able to apply, making use of cutting-edge fields like deep reinforcement learning and computer vision. We’re also proud that the project traveled a much further distance than originally anticipated -- we initially set out to create a gaze-controlled version of Space Invaders you could play with your eyes, and were ultimately able to combine so much more than that.

## What we learned

We both learned a lot more about game creation and rendering in Python, as well as technologies like gaze tracking.
And of course, that the real treasure was friendship all along 😄

## What's next for Space Invaders Invader

Looking forward, we’re hoping to polish up the 2-player version of the game by optimizing the eye-tracking logic (it currently runs very slowly and makes the game difficult to play). We’d also like to robustify the Family Feud answer evaluator to better check for semantic similarity between the player’s answers and accepted solutions (e.g., that “kids” and “children” are the same answer) and improve the UI/UX for a more accessible and aesthetically pleasing experience. 
Another future direction we’re considering is bringing the game to the physical world, and potentially hook up the AI agent to some fake physical eyes that move around while playing the game.
