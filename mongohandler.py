import pymongo
from bson.objectid import ObjectId

class mongoDatabase:
    def __init__(self, dbname, host = "localhost", port = 27017):

        self.client = pymongo.MongoClient(f"mongodb://{host}:{port}/")

        
        dblist = self.client.list_database_names()
        if dbname in dblist:
            print("Connecting to existing database")
            self.db = self.client[dbname]

            self.categories = self.db["categories"]
            self.locations = self.db["locations"]
            self.items = self.db["items"]
            self.suppliers = self.db["suppliers"]
            
        else:
            print("Creating new database")
            if self.createNewStructure(dbname):
                print("New Database Created")
            else:
                print("Issue in creating database")


    def createNewStructure(self, dbname):

        self.db = self.client[dbname]

        sample_categories = [{"category":"Purchase"},
                              {"category":"Fabrication"}]
        sample_locations = [{"location":"Location 1"},
                            {"location":"Locaiton 2"},
                            {"location":"Locaiton 3"}]
        sample_supplier = [{"supplier":"Grand Brass Lamp Parts LLC."},
                            {"supplier":"TUNGSTENE"}]

        sample_item = {"partNumber" : "P-32-001",
                       "primaryImage" : "P-32-001.jpg",
                       "category" : "Purchase",
                       "supplier" : "TUNGSTENE",
                       "model" : "AB472",
                       "priceCAD" : 0.00,
                       "priceUSD" : 2.00,
                       "description" :
                       "1/8ips Female Threaded 90 Degree Straight Armback - Unfinished Brass"}

        self.categories = self.db["categories"]
        self.locations = self.db["locations"]
        self.suppliers = self.db["suppliers"]
        self.items = self.db["items"]

        cat = self.categories.insert_many(sample_categories)
        loc = self.locations.insert_many(sample_locations)
        sup = self.suppliers.insert_many(sample_supplier)
        item = self.items.insert_one(sample_item)
        
        self.insert_log(cat)
        self.insert_log(loc)
        self.insert_log(sup)
        
        return self.db
        
    def insert_log(self,inserted):
        print("[!]", len(inserted.inserted_ids), "entries inserted")

    def getByPartId(self, pid):
        query = {"_id" : pid}
        return self.items.find_one(query)

    def getByPart(self, part):
        query = {"partNumber" : part}
        return self.items.find_one(query)

    def getAllParts(self):
        return self.items.distinct("partNumber")

    def getAllCategories(self):
        return self.categories.distinct("category")
        
    def getAllLocations(self):
        return self.locations.distinct("location")

    def getAllSuppliers(self):
        return self.suppliers.distinct("supplier")


    def updatePartbyId(self, doc, data):

        toupdate = {'_id' : ObjectId(doc)}
        newdata = {'$set': data}

        res = self.items.update_one(toupdate, newdata)

        return res

    def insertNewItem(self, data):
        
        newdata = {'$set': data}

        res = self.items.insert_one(data)

        return res

    def getPartList(self, search):

        query = {'partNumber': {'$regex': search}}

        projection = {'partNumber':1}

        cursor = self.items.find(query, projection).sort('partNumber')

        return list(cursor)

        
    
if __name__ == "__main__":
    db = mongoDatabase("inventory")
    db.getByPart("P-32-001")
    db.getPartList('P')

