from models import *
import streamlit as st

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "db_obj" not in st.session_state:
    st.session_state.db_obj = None

try:
    credentials = load_credentials('creds.json')
except Exception as e:
    st.error(f"Failed to load credentials: {e}")
    st.stop()

model_name = "meta/llama-3.1-8b-instruct"
sql_sys_prompt = "You are an expert coding AI. Respond only in valid MySQL statements; no narration whatsoever."

if not st.session_state.authenticated:
    st.subheader("Connect to Database")
    host = st.text_input("Host", placeholder="e.g., localhost")
    user = st.text_input("User", placeholder="e.g., admin")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    if st.button("Connect"):
        try:
            db_obj = create_database("chatsql", host, user, password)
            if db_obj:
                st.success("Connected to the database!")
                st.session_state.authenticated = True
                st.session_state.db_obj = db_obj
            else:
                st.error("Failed to connect to the database. Check your credentials.")
        except Exception as e:
            st.error(f"Error connecting to the database: {e}")

if st.session_state.authenticated and st.session_state.db_obj:
    st.subheader("Chat with Database")

    try:
        schema = get_database_schema_wrapper(st.session_state.db_obj, "chatsql")
    except Exception as e:
        st.error(f"Failed to load database schema: {e}")
        st.stop()

    user_input = st.text_input("You:", placeholder="Type your message here...")

    if st.button("Send"):
        if user_input.strip():
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            chain = generate_chain(model_name, sql_sys_prompt)

            if "Error" not in chain:
                try:
                    response = execute_sql_chain(chain, st.session_state.db_obj, schema, user_input)

                    if response:  # If query execution returns data
                        st.session_state.chat_history.append({"role": "assistant", "content": "Query executed successfully."})
                        st.write("**Query Result:**")

                        # Display each table result as a dataframe
                        for idx, df in enumerate(response):
                            st.write(f"**Table {idx + 1}:**")
                            st.dataframe(df)  # Use st.table(df) for static rendering
                    else:
                        st.warning("Query returned no results.")
                except Exception as e:
                    st.error(f"Error executing query: {e}")
            else:
                st.error(chain)

    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        elif message["role"] == "assistant":
            st.markdown(f"**LLM:** {message['content']}")
