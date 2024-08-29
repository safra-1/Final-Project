from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

news = {
    1:
    {
        "id":1,
        "title": "Top 10 programming language",
        "content": "Python is the most popular programming language",
        "author": "Kalim"
    }, 
    2:
    {
        "id":2,
        "title": "LLM race in modern era",
        "content": "Content on modern LLM models",
        "author": "Ibrahim"
    }, 
    3:
    {
        "id":3,
        "title": "Latest LLM model from Mistral!!! ",
        "content": "Content on modern LLM models both close & open source",
        "author": "Kalim"
    }, 
    4:
    {
        "id":4,
        "title": "What's the Google calls on LLM!!!",
        "content": "Content on modern LLM models both close & open source",
        "author": "Ema"
    }
        
}

#pydantic model use korle wrong input dile error dekhabe
class News(BaseModel):
    title: str
    content: str | None = None
    author: str

class UpdateNews(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    
    
#Query parameter(question mark diye jodi kono query korte chai)
@app.get("/news/{author}")
def get_news_by_author(author: str, title_contains: str = None):
    
    filtered_news = [news for news in news.values() if news["author"].lower()==author.lower()]

    if title_contains:
        filtered_news_title = [news for news in filtered_news if title_contains.lower() in news["title"].lower()]
        return filtered_news_title
    else:
        return filtered_news

#normal endpoint to show all news
@app.get("/news")
def get_news():
    return news


#url er moddhe dynamic kono value thakle shetake path parameter bole. (dynamic parameter)
@app.get("/news/{id}")
def get_news_by_id(id: int):
    single_news = news.get(id, None)
    if single_news:
        return single_news
    return {"message": f"News item of id {id} not found"}

@app.post("/create_news")
def create_news(input_news: News):
    id =  max(news.keys())+1
    news[id] = {
        "id":id,
        "title": input_news.title,
        "content": input_news.content,
        "author": input_news.author
    }
    return(news[id])

@app.put("/update_news/{id}")
def update_news(id: int, input: UpdateNews):
    if id not in news:
        return {"message": f"News item of id {id} not found"}
    
    if input.title is not None:
        news[id]["title"] = input.title
    if input.content is not None:
        news[id]["content"] = input.content
    if input.author is not None:
        news[id]["author"] = input.author
        
    return news[id]

@app.delete("/delete_news/{id}")
def update_news(id: int):
    if id not in news:
        return {"message": f"News item of id {id} not found"}
    
    del news[id]
    return {"message": "News Deleted Successfully"}

if __name__ == '__main__':
    uvicorn.run("basic:app", host='localhost', port=8000, reload = True)