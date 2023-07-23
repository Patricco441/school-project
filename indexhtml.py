css = '''
<style>
body {
    background-color: #f5f5f5;
    font-family: Arial, sans-serif;
}

.chat-message {
    width: 60%;
    padding: 10px;
    margin-bottom: 10px;
    border-radius: 10px;
    font-size: 16px;
    line-height: 1.5;
}

.bot {
    margin-left: auto;
    background-color: #e6e6e6;
    color: #333;
}

.user {
    margin-right: auto;
    background-color: #0084ff;
    color: white;
}

.message {
    word-wrap: break-word;
}
</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="message">{{MSG}}</div>
</div>
'''