import wolframalpha
import wikipedia
import wx
from gtts import gTTS
import os
import random
import requests
import json
# import pyglet
from googletrans import Translator
import vlc
import pafy
import calendar
import datetime
from youtube_search import YoutubeSearch
import sys

class SecondFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='Help')
        panel = wx.Panel(self)
        lbl_string = 'Type "weather <city name>" to get info about weather.\n'
        lbl_string += 'Type "youtube <search keywords>" to play Youtube videos.\n'
        lbl_string += 'Type "translate <text> <destination language code>" to translate.\n\tEx: translate Hello vi\n'
        lbl_string += 'Type a math expression to get a solution.'
        lbl = wx.StaticText(panel, label=lbl_string)

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None,
            pos=wx.DefaultPosition, size=wx.Size(450, 400),
            style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION |
            wx.CLOSE_BOX | wx.CLIP_CHILDREN, title='PyAd')
        panel = wx.Panel(self)
#         sys.stdout = self;
#         Adjust sizer
        my_sizer = wx.BoxSizer(wx.VERTICAL)

        lbl_string = 'Hi, Im PyAd. Ask me something?\n'
        lbl_string += 'Type "weather <city name>" to get info about weather.\n'
        lbl_string += 'Type "youtube <search keywords>" to play Youtube videos.\n'
        lbl_string += 'Type "translate <text> <destination language code>" to translate.\n\tEx: translate Hello vi\n'
        lbl_string += 'Type a math expression to get a solution.'
        lbl = wx.StaticText(panel, label=lbl_string)
        my_sizer.Add(lbl, 0, wx.ALL, 5)

        # Menu bar
        # menubar = wx.MenuBar()
        # fileMenu = wx.Menu()
        # fileItem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        # menubar.Append(fileMenu, '&File')
        # self.SetMenuBar(menubar)

        # self.Bind(wx.EVT_MENU, self.OnQuit, fileItem)

        # Add help button
        help_button = wx.Button(panel, label = 'Help')
        help_button.Bind(wx.EVT_BUTTON, self.HelpButton)
        my_sizer.Add(help_button, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

#         Add text block
        self.txt = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER, size=(400, 50))
        self.txt.SetFocus()
        self.txt.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
        my_sizer.Add(self.txt, 0, wx.ALL, 5)

#         Add voice button
        speaker_pic = wx.Bitmap("speaker_icon.jpg", wx.BITMAP_TYPE_ANY)
        voice_button = wx.Button(panel, label ="Voice")
        voice_button.SetBitmap(speaker_pic)
        voice_button.Bind(wx.EVT_BUTTON, self.OnEnterVoice)
        my_sizer.Add(voice_button, 0, wx.ALL | wx.ALIGN_LEFT, 5)

#         Add KKK button
        KKK_pic = wx.Bitmap("KKK_icon.png", wx.BITMAP_TYPE_ANY)
        KKK_button = wx.Button(panel, label='Play KKK!')
        KKK_button.SetBitmap(KKK_pic)
        KKK_button.Bind(wx.EVT_BUTTON, self.On_Press_KKK)
        my_sizer.Add(KKK_button, 0, wx.ALL | wx.CENTER, 5)

#         Add Calendar button
        calendar_pic = wx.Bitmap("calendar_icon.png", wx.BITMAP_TYPE_ANY)
        calendar_button = wx.Button(panel, label='Calendar')
        calendar_button.SetBitmap(calendar_pic)
        calendar_button.Bind(wx.EVT_BUTTON, self.get_calendar)
        my_sizer.Add(calendar_button, 0, wx.ALL | wx.CENTER, 5)

#         Set background color
        self.SetBackgroundColour('gray')
        # self.SetBackgroundColour('CADET BLUE')
        panel.SetSizer(my_sizer)

#         log = wx.TextCtrl(panel, wx.ID_ANY, size=(300,100), style=style);
#         sys.stdout = log;

        self.Show()

    def HelpButton (self, event):
        frame = SecondFrame();
        frame.Show()

    #   Get user's input and return info
    def OnEnter(self, event):
        input_ = self.txt.GetValue()
        input_ = input_.lower()
        raw_input_ = str(self.txt.GetValue())

        first_kw = str(raw_input_).split()[0]
        if first_kw == 'weather':
        # if raw_input_ == 'weather':
            api_weather_key = "7b0d74a745885b0d104caf540568ed8c"
            base_url = "http://api.openweathermap.org/data/2.5/weather?"

            # city_name = input("City's name: ")
            city_name_parts = str(raw_input_).split()[1:]
            city_name = ""
            for part in city_name_parts:
                city_name += ""
                city_name += part
            complete_url = base_url + "appid=" + api_weather_key + "&q=" \
            + city_name

            # get method of requests module
            # return response object
            response = requests.get(complete_url)

            # json method of response object convert json format data into
            # python format data
            x = response.json()

            # Now x contains list of nested dictionaries
            # Check the value of "cod" key is equal to "404", means city is
            # found otherwise, city is not found
            if x["cod"] != "404":
                # store the value of "main" key in variable y
                y = x["main"]
                # store the value corresponding to the "temp" key of y
                current_kevin_temperature = y["temp"]
                current_temperature = y['temp'] - 273
                current_temperature = round(current_temperature, 1)
                # store the value corresponding to the "pressure" key of y
                current_pressure = y["pressure"]
                # store the value corresponding to the "humidity" key of y
                current_humidiy = y["humidity"]
                # store the value of "weather" key in variable z
                z = x["weather"]
                # store the value corresponding to the "description" key at
                # the 0th index of z
                weather_description = z[0]["description"]

                answer = str(city_name) + "\nTemperature (in Celcius) = " + str(current_temperature) + "\nAtmospheric pressure (in hPa unit) = " + str(current_pressure) + "\nHumidity (in percentage) = " + str(current_humidiy) + "\nDescription = " + str(weather_description)
                print(answer)

            else:
                print(" City Not Found ")

            return None

        elif first_kw == 'youtube':
            search_term = ""
            for word in str(raw_input_).split():
                search_term += word + " "
            results = YoutubeSearch(search_term, max_results=10).to_dict()
            url_code = results[0]['id']
            url = "https://www.youtube.com/watch?v=" + url_code
            # creating pafy object of the video
            video = pafy.new(url)
            # getting best stream
            best = video.getbest()
            # creating vlc media player object
            media = vlc.MediaPlayer(best.url)
            # start playing video
            media.play()

        elif first_kw == 'translate':
            translate_lang = str(raw_input_).split()[-1]
            translator = Translator()
            translations = translator.translate(str(raw_input_).split()[1:-1], dest=translate_lang)
            origin = ''
            answer = ''
            for translation in translations:
                origin += translation.origin + ' '
                answer += translation.text + ' '
            print(origin, ' -> ', answer)

            return None

        else:
            try:
                # wolframalpha
                app_id = 'WTRAQ5-VR7PE9EHYH'
                client = wolframalpha.Client(app_id)

                res = client.query(input_)
                answer = next(res.results).text
                print(type(res.results[0]))
                print(answer)

            except:
                # wikipedia
                print(wikipedia.summary(input_))

    def OnEnterVoice(self, event):
        input_ = self.txt.GetValue()
        input_ = input_.lower()
        raw_input_ = str(self.txt.GetValue())

        first_kw = str(raw_input_).split()[0]
        if first_kw == 'weather':
            api_weather_key = "7b0d74a745885b0d104caf540568ed8c"
            base_url = "http://api.openweathermap.org/data/2.5/weather?"

            city_name_parts = str(raw_input_).split()[1:]
            city_name = ""
            for part in city_name_parts:
                city_name += ""
                city_name += part
            complete_url = base_url + "appid=" + api_weather_key + "&q=" + city_name

            response = requests.get(complete_url)

            x = response.json()

            if x["cod"] != "404":

                y = x["main"]

                current_kevin_temperature = y["temp"]
                current_temperature = y['temp'] - 273
                current_temperature = round(current_temperature, 1)
                current_pressure = y["pressure"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]

                answer = str(city_name) + "\nTemperature (in Celcius) = " + str(current_temperature) + "\nAtmospheric pressure (in hPa unit) = " + str(current_pressure) + "\nHumidity (in percentage) = " + str(current_humidiy) + "\nDescription = " + str(weather_description)
                print(answer)
                gtts_obj = gTTS(answer, lang='en')
                gtts_obj.save('gtts_obj.mp3')
                os.system('gtts_obj.mp3')

            else:
                print(" City Not Found ")
                gtts_obj = gTTS("City Not Found", lang='en')
                gtts_obj.save('gtts_obj.mp3')
                os.system('gtts_obj.mp3')
            return None

        elif first_kw == 'youtube':
            url = str(raw_input_).split()[1]
            results = YoutubeSearch(str(raw_input_).split()[1], max_results=10).to_dict()
            url_code = results[0]['id']
            url = "https://www.youtube.com/watch?v=" + url_code
            # creating pafy object of the video
            video = pafy.new(url)
            # getting best stream
            best = video.getbest()
            # creating vlc media player object
            media = vlc.MediaPlayer(best.url)
            # start playing video
            media.play()

        elif first_kw == 'translate':
            translate_lang = str(raw_input_).split()[-1]
            translator = Translator()
            translations = translator.translate(str(raw_input_).split()[1:-1], dest=translate_lang)
            origin = ''
            answer = ''
            for translation in translations:
                origin += translation.origin + ' '
                answer += translation.text + ' '
            print(origin, ' -> ', answer)

            gtts_obj = gTTS(answer, lang=translate_lang)
            gtts_obj.save('gtts_obj.mp3')
            os.system('gtts_obj.mp3')

            return None

        else:
            try:
                # wolframalpha
                app_id = 'WTRAQ5-VR7PE9EHYH'
                client = wolframalpha.Client(app_id)
                res = client.query(input_)
                answer = next(res.results).text
                print(answer)

                # Play sound that reads the answer
                gtts_obj = gTTS(answer, lang='en')
                gtts_obj.save('gtts_obj.mp3')
                os.system('gtts_obj.mp3')
                # os.remove('gtts_obj.mp3')
            except:
                # wikipedia
                print(wikipedia.summary(input_))

                # Play sound that reads the answer
                gtts_obj = gTTS(wikipedia.summary(input_, sentences=3), lang='en')
                gtts_obj.save('gtts_obj.mp3')
                os.system('gtts_obj.mp3')

    def On_Press_KKK(self, event):
        deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
        player_hand = []
        dealer_hand = []
        for i in range(3):
            card = random.choice(deck)
            player_hand.append(card)
            another_card = random.choice(deck)
            dealer_hand.append(another_card)
        print('You got ' + str(player_hand[0]) + ', ' + str(player_hand[1]) + ' and ' + str(player_hand[2]) + '.\n')
        print('The Dealer got ' + str(dealer_hand[0]) + ', ' + str(dealer_hand[1]) + ' and ' + str(dealer_hand[2]) + '.\n')
        total_player = 0
        total_dealer = 0
        for card in player_hand:
            if card == 'J' or card == 'Q' or card == 'K':
                total_player += 10
            elif card == 'A':
                total_player += 1
            else:
                total_player += card
        for card in dealer_hand:
            if card == 'J' or card == 'Q' or card == 'K':
                total_dealer += 10
            elif card == 'A':
                total_dealer += 1
            else:
                total_dealer += card
        if total_player > total_dealer:
            print('Aha! You win!')
        elif total_player < total_dealer:
            print('Aha! You lose!')
        else:
            print('Aha! Draw!')

#     Get calendar
    def get_calendar(self, event):
        today_date = datetime.datetime.today()
        today_year = today_date.year
        today_month = today_date.month
        print(calendar.month(today_year, today_month))

if __name__ == '__main__':
    app = wx.App(True)
    frame = MyFrame()
    app.MainLoop()

# Add google maps feature
# Add dropdown menu
# Add visual
# Add meme generator
# Add cre
# Add help
# Customize output windows
