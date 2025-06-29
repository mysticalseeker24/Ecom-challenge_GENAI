import pandas as pd

def load_and_clean_data(csv_path: str) -> list[str]:
    df = pd.read_csv(csv_path)
    df.dropna(subset=["title", "description", "price", "average_rating"], inplace=True)
    df = df[df["price"].apply(lambda x: isinstance(x, (int, float)) or str(x).replace(".", "", 1).isdigit())]
    df = df[df["average_rating"].apply(lambda x: isinstance(x, (int, float)) or str(x).replace(".", "", 1).isdigit())]

    documents = []
    for _, row in df.iterrows():
        doc_text = (
            f"Category: {row.get('main_category', '')}\n"
            f"Title: {row['title']}\n"
            f"Features: {row.get('features', '')}\n"
            f"Description: {row['description']}\n"
            f"Price: ${row['price']}\n"
            f"Average Rating: {row['average_rating']}\n"
        )
        documents.append(doc_text)

    return documents
