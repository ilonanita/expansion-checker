streamlit.errors.StreamlitDuplicateElementId: This app has encountered an error. The original error message is redacted to prevent data leaks. Full error details have been recorded in the logs (if you're on Streamlit Cloud, click on 'Manage app' in the lower right of your app).

Traceback:
File "/mount/src/expansion-checker/app.py", line 81, in <module>
    spark = dot_rating(
        "🔥 Spark",
        "Does this ignite intellectual, emotional, or sensual aliveness?"
    )
File "/mount/src/expansion-checker/app.py", line 66, in dot_rating
    value = st.radio(
        "",
    ...<3 lines>...
        format_func=lambda x: "○"
    )
File "/home/adminuser/venv/lib/python3.13/site-packages/streamlit/runtime/metrics_util.py", line 532, in wrapped_func
    result = non_optional_func(*args, **kwargs)
File "/home/adminuser/venv/lib/python3.13/site-packages/streamlit/elements/widgets/radio.py", line 364, in radio
    return self._radio(
           ~~~~~~~~~~~^
        label=label,
        ^^^^^^^^^^^^
    ...<13 lines>...
        width=width,
        ^^^^^^^^^^^^
    )
    ^
File "/home/adminuser/venv/lib/python3.13/site-packages/streamlit/elements/widgets/radio.py", line 421, in _radio
    element_id = compute_and_register_element_id(
        "radio",
    ...<9 lines>...
        width=width,
    )
File "/home/adminuser/venv/lib/python3.13/site-packages/streamlit/elements/lib/utils.py", line 265, in compute_and_register_element_id
    _register_element_id(ctx, element_type, element_id)
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.13/site-packages/streamlit/elements/lib/utils.py", line 150, in _register_element_id
    raise StreamlitDuplicateElementId(element_type)
