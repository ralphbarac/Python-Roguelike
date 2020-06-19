import tcod

from game_messages import Message

# There may be 'errors' highlighted in areas with the code "self.owner". This is OK because these elements all have owners at runtime the IDE just doesn't 
# realize it. This is what happens when you use composition instead of inheritance.

class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []
    
    def add_item(self, item):
        results = []

        if len(self.items) >= self.capacity:
            results.append({
                'item_added': None,
                'message': Message('Your inventory is too full to pick any more items up!', tcod.yellow)
            })
        else:
            results.append({
                'item_added': item,
                'message': Message('You pick up the {0}.'.format(item.name), tcod.blue)
            })

            self.items.append(item)
        
        return results
    
    def use(self, item_entity, **kwargs):
        results = []

        item_component = item_entity.item

        if item_component.use_function is None:
            page_component = item_entity.page

            if page_component:
                results.append({'equip': item_entity})
            else:
                results.append({'message': Message('The {0} cannot be used'.format(item_entity.name), tcod.yellow)})

        else:
            kwargs = {**item_component.function_kwargs, **kwargs}
            item_use_results = item_component.use_function(self.owner, **kwargs)

            for item_use_result in item_use_results:
                if item_use_result.get('consumed'):
                    self.remove_item(item_entity)
            
            results.extend(item_use_results)
        
        return results
    
    def remove_item(self, item):
        self.items.remove(item)

    def drop_item(self, item):
        results = []

        if(self.owner.book.ele_1 == item or 
           self.owner.book.ele_2 == item or 
           self.owner.book.life == item or 
           self.owner.book.vision == item or 
           self.owner.book.alt == item):

            self.owner.book.toggle_page(item)

        item.x = self.owner.x
        item.y = self.owner.y

        self.remove_item(item)
        results.append({'item_dropped': item, 'message': Message('You dropped the {0}'.format(item.name), tcod.yellow)})

        return results