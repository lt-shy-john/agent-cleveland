# Agent Cleveland
Agent Cleveland is your buddy to learn a new language. 

It is part of Kaggle's 5-Day AI Agents Intensive Course with Google submission. 

### Problem Statement


### Solution Statement


### Architecture
![](public/AgentClevelandArchitecture.png)

### Essential Tools and Utilities

### Conclusion

## Installation
This project was built against Python 3.11.3. To start, 
1. Install the required packages using `pip install -r requirements.txt`. 
2. Add the API key in environment variables. 

To run the agent, please the following command at the root folder of this project: 
`adk create lang-agent --api_key $GOOGLE_API_KEY`. 

> [!NOTE]
> Make sure your `$GOOGLE_API_KEY` is set in your computer. 

To use the agent, run the ADK web UI using the following command: 

`adk web`

### Debugging
This project has configurations on the log while using the agent. Run the ADK web UI using the following command: 

`adk web --log_level DEBUG`


## Project Structure
The project is organized as follows:
* `lang-agent/`
  * `agent.py`
  * `config.py`
  * `tools.py`
* `plugin/`
  * `CountInvocationPlugin.py`
* `public/`
* `test/`

## Workflow
The agent works as following: 
1. The user will ask help for one language. To do this, use the `find_lang_agent` agent. 
2. You then ask what the user want to do today. They will prompt you based on the following options: 
   *  **Teach** You provide them one example of using the language. 
   *  **Conversation** You and the user talks with the language casually. 
   *  **Quiz** You ask the user a word from the language.  
