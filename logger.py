from datetime import datetime


def log_query(query, answer):
    try:
        with open("query_logs.txt", "a", encoding="utf-8") as file:
            file.write(
                f"Time: {datetime.now()}\n"
                f"Question: {query}\n"
                f"Answer: {answer}\n"
                f"{'-' * 50}\n"
            )

    except Exception as e:
        print("Logging Error:", e)