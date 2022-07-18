#importações
import disnake
from disnake.ext import commands
from disnake.ui import Button

import mysql.connector

#   Inicialização do bot
intents = disnake.Intents().default()
intents.members = True
client = commands.Bot(intents=intents, test_guilds=["ID do seu servidor do discord AQUI, caso tenha mais adicione na lista!!!"])

#   Banco de dados 
host="localhost"
user="root"
password=""
database="LeafCode_DataBase"

#ANTENÇÂO caso o nome da table seja alterada no arquivo config.yml dos plugins(LeafCore e LeafTags) altere aqui abaixo também!
tables_core="leafcore_users"
tables_tags="leaftags_users"

#   Comando em slash(/) responsavel por pegar as informações do player nos plugins da LeafCodeBR
@client.slash_command(name='info_player', description="Pegue informações de player nos plugins da LeafCode")
async def get_player(inter, nick: str):
    
    data_base = mysql.connector.connect(host=host, user=user, password=password, database=database) #conexão ao banco de dados
    cursor_core = data_base.cursor() #Cursor para a table do LeafCore
    cursor_tags = data_base.cursor() #Cursor para a table do LeafTags
    
    cursor_core.execute(f"SELECT * FROM {tables_core} WHERE username = '{nick}'") #Execução do comando para pegar as informações do player no banco de dados do leafCore
    
    result_core = cursor_core.fetchone() #Compilação dos resultados em tupla
    cursor_tags.execute(f"SELECT * FROM {tables_tags} WHERE UUID='{result_core[0]}'") #Execução do comando para pegar a tag do player pelo UUID no banco de dados do LeafTags
    result_tags = cursor_tags.fetchone() #Compilação dos resultados em tupla
    
    #Apresentão das informações para o usuário final
    embed = disnake.Embed( #Crição do embed
        title=f"Informações do player {nick}",
        description=f"Essas são as informações do player {nick} nos plugins da LeafCodeBR\n",
        color=disnake.Color.from_rgb(121, 53, 216)
    )
    
    #Adição de campos com as informações no embed
    embed.add_field(name="UUID", value=result_core[0], inline=False)
    embed.add_field(name="Ultima Tag", value=result_tags[1], inline=False)
    embed.add_field(name="Ultimo login", value=result_core[4], inline=False)
    embed.add_field(name="Primeiro login", value=result_core[3], inline=False)

    embed.set_thumbnail(url="https://cdn.discordapp.com/icons/901627752392843296/a_a7972abe05d15cad3fc3c0616dfebebd.gif?size=2048")
    
    #Resposta ao comando enviando pelo usuário como ephemeral(visivel apenas para o usário que executou o comando)
    await inter.response.send_message(embed=embed, ephemeral=True, components=[[Button(style=disnake.ButtonStyle.link, url="https://discord.gg/WXJ6K2RRM2", label="LeafCodeBR"), Button(style=disnake.ButtonStyle.link, url="https://discord.gg/PzKVGHJd2x", label="EvoCloud")]])

#Inicia o seu bot com o token especifiado
client.run("<seu token>")







