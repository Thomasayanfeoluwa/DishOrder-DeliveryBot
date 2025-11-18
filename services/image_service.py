import os

class DishImageService:
    def __init__(self):
        self.dish_images = {
            # 🍲 SOUPS AND STEWS
            
            ### Egusi Soups
            "Egusi Soup with Beef": "https://i.ibb.co.com/0jV7rZ6/egusi.jpg",
            "Egusi Soup with Fish": "https://i.ibb.co.com/0jV7rZ6/egusi.jpg", 
            "Egusi Soup with Assorted Meat": "https://i.ibb.co.com/0jV7rZ6/egusi.jpg",
            "Egusi Soup with Goat Meat": "https://i.ibb.co.com/0jV7rZ6/egusi.jpg",

            ### Ogbono Soups
            "Ogbono Soup with Beef": "https://i.ibb.co.com/7pZJq8m/ogbono.jpg",
            "Ogbono Soup with Fish": "https://i.ibb.co.com/7pZJq8m/ogbono.jpg",
            "Ogbono Soup with Okporoko (Stockfish)": "https://i.ibb.co.com/7pZJq8m/ogbono.jpg",

            ### Vegetable Soups
            "Vegetable Soup (Efo Riro)": "https://i.ibb.co.com/5Y6ZXb5/vegetable-soup.jpg",
            "Bitterleaf Soup (Ofe Onugbu)": "https://example.com/bitterleaf-soup.jpg",
            "Oha Soup": "https://example.com/oha-soup.jpg",
            "Afang Soup": "https://i.ibb.co.com/7pZJq8m/afang.jpg",
            "Edikaikong Soup": "https://i.ibb.co.com/3pL7d2k/edikaikong.jpg",

            ### Other Soups
            "White Soup (Ofe Nsala)": "https://example.com/white-soup.jpg",
            "Banga Soup": "https://i.ibb.co.com/0jV7rZ6/banga.jpg",
            "Pepper Soup (Goat)": "https://example.com/pepper-soup-goat.jpg",
            "Pepper Soup (Fish)": "https://example.com/pepper-soup-fish.jpg",

            # 🍚 SWALLOWS (STARCHY FOODS)
            "Pounded Yam": "https://i.ibb.co.com/0jV7rZ6/pounded-yam.jpg",
            "Fufu": "https://i.ibb.co.com/8jD8Y6g/fufu.jpg",
            "Eba": "https://i.ibb.co.com/7pZJq8m/eba.jpg",
            "Amala": "https://i.ibb.co.com/3pL7d2k/amala.jpg",
            "Semovita": "https://i.ibb.co.com/5Y6ZXb5/semo.jpg",
            "Wheat": "https://example.com/wheat-swallow.jpg",

            # 🍚 RICE DISHES
            
            ### Jollof Rice
            "Plain Jollof Rice": "https://i.ibb.co.com/0jV7rZ6/jollof-protein.jpg",
            "Jollof Rice with Chicken": "https://i.ibb.co.com/0jV7rZ6/jollof-protein.jpg",
            "Jollof Rice with Beef": "https://i.ibb.co.com/0jV7rZ6/jollof-protein.jpg",
            "Party Jollof Rice": "https://i.ibb.co.com/0jV7rZ6/jollof-protein.jpg",

            ### Other Rice Dishes
            "Fried Rice with Chicken": "https://i.ibb.co.com/5Y6ZXb5/fried-rice.jpg",
            "Fried Rice with Beef": "https://i.ibb.co.com/5Y6ZXb5/fried-rice.jpg",
            "Coconut Rice": "https://example.com/coconut-rice.jpg",
            "Ofada Rice with Ayamase Sauce": "https://example.com/ofada-rice.jpg",
            "White Rice and Stew": "https://i.ibb.co.com/3pL7d2k/white-rice-stew.jpg",

            # 🍗 PROTEIN AND MEAT DISHES
            
            ### Chicken
            "Grilled Chicken (1/4)": "https://i.ibb.co.com/7pZJq8m/chicken.jpg",
            "Grilled Chicken (1/2)": "https://i.ibb.co.com/7pZJq8m/chicken.jpg",
            "Fried Chicken (1/4)": "https://i.ibb.co.com/7pZJq8m/chicken.jpg",
            "Chicken Stew": "https://i.ibb.co.com/7pZJq8m/chicken.jpg",

            ### Beef and Goat
            "Beef Stew": "https://i.ibb.co.com/9hJq8fL/assorted-meat.jpg",
            "Grilled Beef (Suya Style)": "https://example.com/suya.jpg",
            "Goat Meat Pepper Soup": "https://example.com/pepper-soup-goat.jpg",
            "Nkwobi (Spicy Cow Foot)": "https://example.com/nkwobi.jpg",

            ### Fish and Seafood
            "Grilled Tilapia": "https://i.ibb.co.com/5nFz8H/tilapia.jpg",
            "Grilled Catfish (Point & Kill)": "https://i.ibb.co.com/7pZJq8m/catfish.jpg",
            "Fried Fish": "https://example.com/fried-fish.jpg",
            "Fish Stew": "https://example.com/fish-stew.jpg",

            # 🍢 SNACKS AND STREET FOOD
            
            ### Suya and Barbecue
            "Beef Suya": "https://example.com/suya.jpg",
            "Chicken Suya": "https://example.com/chicken-suya.jpg",
            "Ram Suya": "https://example.com/ram-suya.jpg",
            "Kilishi (Dried Suya)": "https://example.com/kilishi.jpg",

            ### Small Chops
            "Samosa (2 pieces)": "https://example.com/samosa.jpg",
            "Spring Rolls (3 pieces)": "https://example.com/spring-rolls.jpg",
            "Puff Puff (5 pieces)": "https://example.com/puff-puff.jpg",
            "Meat Pie": "https://example.com/meat-pie.jpg",
            "Scotch Egg": "https://example.com/scotch-egg.jpg",

            ### Traditional Snacks
            "Akara (Bean Cake)": "https://example.com/akara.jpg",
            "Moi Moi": "https://example.com/moi-moi.jpg",
            "Roasted Plantain (Bole)": "https://example.com/boli.jpg",
            "Fried Plantain (Dodo)": "https://example.com/dodo.jpg",

            # 🥗 SIDES AND EXTRAS
            "Fried Plantain": "https://example.com/dodo.jpg",
            "Boiled Plantain": "https://example.com/boiled-plantain.jpg",
            "Boiled Yam": "https://example.com/boiled-yam.jpg",
            "Fried Yam": "https://example.com/fried-yam.jpg",
            "Garden Salad": "https://example.com/garden-salad.jpg",
            "Moin Moin": "https://example.com/moi-moi.jpg",
            "Egg (Fried or Boiled)": "https://example.com/egg.jpg",

            # 🥤 DRINKS AND BEVERAGES
            
            ### Nigerian Traditional Drinks
            "Zobo Drink": "https://i.ibb.co.com/0jV7rZ6/zobo.jpg",
            "Kunu Aya (Tiger Nut Drink)": "https://example.com/kunu-aya.jpg",
            "Fura da Nono": "https://example.com/fura-da-nono.jpg",
            "Chapman": "https://example.com/chapman.jpg",

            ### Fruit Juices
            "Orange Juice": "https://example.com/orange-juice.jpg",
            "Pineapple Juice": "https://example.com/pineapple-juice.jpg",
            "Mango Juice": "https://example.com/mango-juice.jpg",
            "Chapman Special": "https://example.com/chapman-special.jpg",

            ### Soft Drinks and Water
            "Coke (35cl)": "https://i.ibb.co.com/0jV7rZ6/coke.jpg",
            "Fanta (35cl)": "https://i.ibb.co.com/5Y6ZXb5/fanta.jpg",
            "Sprite (35cl)": "https://i.ibb.co.com/3pL7d2k/sprite.jpg",
            "Maltina": "https://example.com/maltina.jpg",
            "Bottled Water (50cl)": "https://i.ibb.co.com/7pZJq8m/water.jpg",

            ### Hot Beverages
            "Tea": "https://example.com/tea.jpg",
            "Coffee": "https://example.com/coffee.jpg",
            "Milo": "https://example.com/milo.jpg",
            "Hot Chocolate": "https://example.com/hot-chocolate.jpg",

            # 🍰 DESSERTS AND SWEETS
            "Chin Chin": "https://example.com/chin-chin.jpg",
            "Puff Puff with Sugar": "https://example.com/puff-puff.jpg",
            "Coconut Candy": "https://example.com/coconut-candy.jpg",
            "Ice Cream (Scoop)": "https://example.com/ice-cream.jpg",
            "Fruit Salad": "https://example.com/fruit-salad.jpg",

            # 🍛 COMBO MEALS
            
            ### Executive Combos
            "Jollof Rice + Chicken + Salad + Drink": "https://i.ibb.co.com/0jV7rZ6/jollof-protein.jpg",
            "Fried Rice + Beef + Plantain + Drink": "https://i.ibb.co.com/5Y6ZXb5/fried-rice.jpg",
            "Pounded Yam + Egusi Soup + Assorted Meat": "https://i.ibb.co.com/0jV7rZ6/pounded-yam.jpg",

            ### Student Combos
            "Jollof Rice + Chicken": "https://i.ibb.co.com/0jV7rZ6/jollof-protein.jpg",
            "Fried Rice + Beef": "https://i.ibb.co.com/5Y6ZXb5/fried-rice.jpg",

            ### Family Packs
            "Family Jollof Rice Pack (Serves 4)": "https://i.ibb.co.com/0jV7rZ6/jollof-protein.jpg",
            "Family Fried Rice Pack (Serves 4)": "https://i.ibb.co.com/5Y6ZXb5/fried-rice.jpg",

            # 🎉 PARTY PACKS
            "Small Party Pack (Serves 10)": "https://example.com/party-pack.jpg",
            "Medium Party Pack (Serves 20)": "https://example.com/party-pack.jpg",
            "Large Party Pack (Serves 50)": "https://example.com/party-pack.jpg"
        }
    
    def get_dish_image(self, dish_name):
        """Get image URL for a dish"""
        # First try exact match
        if dish_name in self.dish_images:
            return self.dish_images[dish_name]
        
        # Then try partial match
        for key in self.dish_images:
            if key.lower() in dish_name.lower():
                return self.dish_images[key]
        
        # If no match found, return None
        return None
    
    def get_images_for_order(self, order_text):
        """Extract dish images from order text"""
        images = []
        order_lower = order_text.lower()
        
        # Check each dish name against the order text
        for dish_name, image_url in self.dish_images.items():
            # Convert dish name to searchable format (remove special characters, prices, etc.)
            search_name = dish_name.split(' - ')[0].split(' (')[0].lower()
            
            if search_name in order_lower:
                if image_url not in images:  # Avoid duplicates
                    images.append(image_url)
        
        return images[:4]  # Max 4 images to avoid clutter
    
    def get_all_dishes_by_category(self):
        """Return dishes organized by category for debugging"""
        categories = {
            "Egusi Soups": [],
            "Ogbono Soups": [],
            "Vegetable Soups": [],
            "Other Soups": [],
            "Swallows": [],
            "Jollof Rice": [],
            "Other Rice Dishes": [],
            "Chicken": [],
            "Beef and Goat": [],
            "Fish and Seafood": [],
            "Suya and Barbecue": [],
            "Small Chops": [],
            "Traditional Snacks": [],
            "Sides and Extras": [],
            "Nigerian Traditional Drinks": [],
            "Fruit Juices": [],
            "Soft Drinks and Water": [],
            "Hot Beverages": [],
            "Desserts and Sweets": [],
            "Executive Combos": [],
            "Student Combos": [],
            "Family Packs": [],
            "Party Packs": []
        }
        
        # This is a helper method to see which dishes have images
        for dish_name, image_url in self.dish_images.items():
            # You would need to map dishes to categories - this is simplified
            print(f"'{dish_name}': '{image_url}',")
        
        return categories