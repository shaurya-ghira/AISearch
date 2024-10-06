from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from summApp.models import Article, MessageHistory
import os
from groq import Groq


client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

class ArticleView(View):
    def get(self, request,topic):
        
        MessageHistory.objects.create(message=f"Article request for topic: {topic}")

        article = Article.objects.filter(topic__iexact=topic).first()

        if article:
            # If article exists, render the saved content
            return render(request, 'summary.html', {'response': article.content, 'topic': topic})
        
        # If article doesn't exist, fetch from API

        article, created = Article.objects.get_or_create(topic=topic)
        
        # if created:
        try:
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"Summarize {topic} in less than 300 words but atleast 250 words.",
                    }
                ],
                model="llama3-8b-8192",
                max_tokens=500 
            )
            article.content = response.choices[0].message.content.strip()
            article.save()

            # output = response.choices[0].message.content
            # return HttpResponse(request,output)
            
            return render(request, 'summary.html', {'response': article.content, 'topic':topic})

        except Exception as e:
            return HttpResponse(f"Error occurred while fetching the summary: {str(e)}", status=500)     
        

    

class LastXMessagesView(View):
    def get(self, request, num_messages):
        messages = MessageHistory.objects.order_by('-created')[:int(num_messages)]
        message_list = [msg.message for msg in messages] 

        return render(request, 'messageHistory.html', {'messages': message_list})