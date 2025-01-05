import aiohttp  # Eşzamansız HTTP istekleri için bir kütüphane
import random
from datetime import datetime,timedelta
import time

class Pokemon:
    pokemons = {}

    # Nesne başlatma (kurucu)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.element = None
        self.move = None
        self.ability = None
        self.hp =random.randint(80,100)
        self.power =random.randint(20,60)
        self.last_feed_time = datetime.now()
         
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]

    async def get_name(self):
        # PokeAPI aracılığıyla bir pokémonun adını almak için eşzamansız bir yöntem
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API'si
        async with aiohttp.ClientSession() as session:  # Bir HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve kodunun çözülmesi
                    return data['forms'][0]['name']  # Bir Pokémon'un adını döndürme
                else:
                    return "Pokeball"  # İstek başarısız olursa varsayılan adı döndürür

    async def info(self):
        # Pokémon hakkında bilgi döndüren bir metot
        if not self.name:
            self.name = await self.get_name()  # Henüz yüklenmemişse bir adın geri alınması
        if not self.element:
            self.element = await self.get_element()
        if not self.move:
            self.move = await self.get_move()

        return f"Pokémonunuzun ismi: {self.name}, \nPokémonunuzun tipi: {self.element}\nPokémonunuzun haraketleri: {self.move}\nPokémonuzun canı: {self.hp}\nPokémonuzun gücü: {self.power}"  # Pokémon'un adını içeren dizeyi döndürür

    async def show_img(self):
        # PokeAPI aracılığıyla bir pokémon görüntüsünün URL'sini almak için eşzamansız bir yöntem
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API'si
        async with aiohttp.ClientSession() as session:  # Bir HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve kodunun çözülmesi
                    return data['sprites']['front_default']  # Bir Pokémon'un adını döndürme
                else:
                    return None  # İstek başarısız olursa varsayılan adı döndürür
                
    async def get_element(self):
        # PokeAPI aracılığıyla bir pokémonun adını almak için eşzamansız bir yöntem
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API'si
        async with aiohttp.ClientSession() as session:  # Bir HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve kodunun çözülmesi
                    return data['types'][0]['type']['name']  # Bir Pokémon'un adını döndürme
                else:
                    return None  # İstek başarısız olursa varsayılan adı döndürür
                
    async def get_move(self):
        # PokeAPI aracılığıyla bir pokémonun adını almak için eşzamansız bir yöntem
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API'si
        async with aiohttp.ClientSession() as session:  # Bir HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve kodunun çözülmesi
                    #print(data['moves'])
                    return data['moves'][0]['move']['name']  # Bir Pokémon'un adını döndürme
                else:
                    return None 
    async def get_ability(self):
            # PokeAPI aracılığıyla bir pokémonun adını almak için eşzamansız bir yöntem
            url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API'si
            async with aiohttp.ClientSession() as session:  # Bir HTTP oturumu açma
                async with session.get(url) as response:  # GET isteği gönderme
                    if response.status == 200:
                        data = await response.json()  # JSON yanıtının alınması ve kodunun çözülmesi
                        #print(data['moves'])
                        return data['ability'][0]['name']  # Bir Pokémon'un adını döndürme
                    else:
                        return None 
    async def attack(self, enemy):
        if isinstance(enemy, Wizard):  # Enemy'nin bir Wizard veri tipi olduğunu (Büyücü sınıfının bir örneği olduğunu) kontrol etme
            sans = random.randint(1, 5) 
            if sans == 1:
                return "Sihirbaz Pokémon, savaşta bir kalkan kullanıldı!"
            
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ne saldırdı\n@{enemy.pokemon_trainer}'nin sağlık durumu{enemy.hp}"
        else:
            enemy.hp = 0
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ni yendi!"

    async def feed(self, feed_interval=20, hp_increase=10):
        current_time = datetime.now()
        delta_time = timedelta(seconds=feed_interval)
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Pokémon'un sağlığı geri yüklendi. Mevcut sağlık: {self.hp}"
        else:
            return f"Pokémonunuzu şu zamana kadar besleyemezsiniz: {current_time+delta_time}"
        
class Wizard(Pokemon):
    async def attack(self, enemy):
        return await super().attack(enemy)
    
    async def feed(self):
        return await super().feed(feed_interval=10)


class Fighter(Pokemon):
    async def attack(self, enemy):
        super_power = random.randint(5, 15)  
        self.power += super_power
        result = await super().attack(enemy)  
        self.power -= super_power
        return result + f"\nDövüşçü Pokémon süper saldırı kullandı. Eklenen güç: {super_power}"
    
    async def feed(self):
        return await super().feed(hp_increase=20)


import asyncio

async def main():
    poke = Pokemon("Ömer")
    wizard = Wizard("username1")
    fighter = Fighter("username2")

    # Pokémon bilgilerini göster
    wizard_info = await wizard.info()
    fighter_info = await fighter.info()
    print(wizard_info)
    print("#" * 10)
    print(fighter_info)
    print("#" * 10)

    poke_info = await poke.info()
    print(poke_info)
    print(await poke.feed())
    print(await wizard.feed())
    print(await fighter.feed())


    time.sleep(10)
    print(await poke.feed())
    print(await wizard.feed())
    print(await fighter.feed())
    time.sleep(10)
    print(await poke.feed())
    print(await wizard.feed())
    print(await fighter.feed())

    # Saldırı senaryosu
    attack_result1 = await wizard.attack(fighter)
    attack_result2 = await fighter.attack(wizard)

    print(attack_result1)
    print(attack_result2)

# asyncio döngüsü ile çalıştır
if __name__ == '__main__':
    asyncio.run(main())