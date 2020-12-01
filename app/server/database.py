import motor.motor_asyncio
from bson.objectid import ObjectId
import re

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.beny

competitors_collection = database.get_collection("competitors")
crawl_collection = database.get_collection("crawl")
shopsadmin_collection = database.get_collection("shopsadmin")
user_collection = database.get_collection("users")
marketplace_collection = database.get_collection("marketplaces")
products_collection = database.get_collection("products")

# helpers

def competitor_helper(competitor) -> dict:
	return {
		"id": str(competitor["_id"]),
		"excluded": competitor["excluded"],
		"seller_url": competitor["seller_url"],
		"n_articles": competitor["n_articles"],
		"eans": competitor["eans"],
		"shop": competitor["shop"],
		"marketplace": competitor["marketplace"],
		"included": competitor["included"],
		"name": competitor["name"],
		"seller_id": competitor["seller_id"],
		"user_email": competitor["user_email"]
	}


def crawl_helper(crawl) -> dict:
	
	crawl_parameters = [
		"_site", "company", "seller_url", "_product", "condition",
		"seller_id", "exclude_shops", "price", "_date_scraped", "raw_price",
	    "url", "currency", "shop", "raw_shipping_time", "_ranking",
	    "_url", "reviews", "exclude", "_search_by", "shipping_cost", "rating"]
	
	crawl_dict = {}
	
	crawls = get_valid_fields(crawl_parameters, crawl_dict, crawl)
	
	return crawls


def shopasadmin_helper(shopsadmin) -> dict:
	
	shopasadmin_parameters = [
		"Markets", "Website", "ID", "Name", "EndDate",
		"StartDate", "License", "Client", "MaxArticles", "Payment"]
	
	shopasadmins = get_valid_fields(shopasadmin_parameters, shopsadmin)
	
	return shopasadmins

def user_helper(user) -> dict:
	
	user_parameters = [
		"_id", "email", "username", "enable", "apikey", "role"]
	
	users = get_valid_fields(user_parameters, user)
	
	return users

def marketplace_helper(market) -> dict:
	
	market_parameters = ["_id", "Name", "ID", "URL"]
	
	marketplaces = get_valid_fields(market_parameters, market)
	
	return marketplaces


def product_helper(product) -> dict:
	
	market_parameters = ["_id", "shop", "marketplace", "ean", "status"]
	
	marketplaces = get_valid_fields(market_parameters, product)
	
	return marketplaces


def get_valid_fields(parameters, obj):
	dict = {}
	for i in parameters:
		if i in obj.keys():
			dict[i] = obj[i]
	
	return dict


# Retrieve all competitors present in the database
async def retrieve_competitors():
	competitors = []
	async for competitor in competitors_collection.find():
		competitors.append(competitor_helper(competitor))
	return competitors


# Retrieve all crawls present in the database
async def retrieve_crawls():
	crawls = []
	async for crawl in crawl_collection.find():
		crawls.append(crawl_helper(crawl))
	return crawls


async def retrieve_competitors():
	shopsadmins = []
	async for shopsadmin in shopsadmin_collection.find():
		shopsadmins.append(shopasadmin_helper(shopsadmin))
	return shopsadmins


# Tasks


# Populate Competitors
async def populate_competitors():
	async for shop in shopsadmin_collection.find():
		client = await get_user(shopasadmin_helper(shop).get("Client"))
		if shop.get("Markets").__class__.__name__ == 'list':
			markets = shop.get("Markets")
		else:
			markets = [shop.get("Markets")]

		for market in markets:
			fetched_market = await get_market(market)
			market_name = fetched_market.get("Name")

			where = {
				"shop": shop.get("ID"),
				"marketplace": fetched_market.get("ID")
			}

			if client:
				where['user_email'] = client.get('email')
			
			eans = await products_collection.find(where).distinct("ean")
			count_eans = len(eans)
			
			print("User email - " + str(where.get('user_email')), end="\n")
			print("Shop - " + str(shop.get("ID")), end="\n")
			print("Marketplace - " + str(market_name), end="\n")
			print("Count eans - " + str(count_eans), end="\n")
			
			pipeline = [
				{
					'$match': {
						'$and': [
							{'shop': shop.get("ID")},
							{
								'_site':
									{'$regex': market_name, "$options": 'i'}
							},
							{'_product': {'$in': eans}},
							{'_company': {'$ne': ''}},
							{
								'exclude':
									{'$exists': True}
							}
						]
					}
				},
				{
					'$project': {
						'shop':  1,
						'_site': 1,
						'_product': 1,
						'company':  1,
						'exclude':  1,
						'seller_id':  1,
						'seller_url': 1,
					}
				},
				{
					'$group': {
						'_id': {
							'company': '$company',
							'exclude': '$exclude',
							'seller_id': '$seller_id',
							'seller_url': '$seller_url',
						},
						'uniq_eans': {'$addToSet': '$_product'}
					}
				}
			]
			
			crawlCursor = crawl_collection.aggregate(pipeline=pipeline)
			
			crawlInfo = {}
			async for item in crawlCursor:
				company = item.get("_id").get("company")
				if not company:
					continue
				
				count = len(item.get('uniq_eans'))
				
				if company not in crawlInfo:
					crawlInfo[company] = {
						"included": 0,
						"excluded": 0,
						"name": company,
						"eans": []
					}
				crawlInfo[company]["seller_id"] = item.get("_id").get("seller_id") or ''
				crawlInfo[company]["seller_url"] = item.get("_id").get("seller_url") or ''
				
				if item.get("_id").get("exclude") == 0:
					crawlInfo[company]["included"] = count
				else:
					crawlInfo[company]["excluded"] = count
				
				crawlInfo[company]["eans"].append(item.get("uniq_eans"))
				
			for key in crawlInfo.keys():
				crawlInfo[key]["n_articles"] = len(crawlInfo[key]["eans"])
				crawlInfo[key]["user_email"] = client.get("email")
				crawlInfo[key]["shop"] = shop.get("ID")
				crawlInfo[key]["marketplace"] = fetched_market.get("ID")
			
			data = crawlInfo.values()
			
			await competitors_collection.delete_many(where)
			print("Removed old data in competitor table", end="\n")
			[await competitors_collection.insert_one(i) for i in data]
			print("Inserted new data in competitor table", end="\n")


async def get_user(client_id):
	async for user in user_collection.find():
		if user_helper(user).get("_id") == ObjectId(client_id):
			return user

	return None


async def get_market(market_id):
	async for market in marketplace_collection.find():
		if marketplace_helper(market).get("_id") == ObjectId(market_id):
			return market

	return None
