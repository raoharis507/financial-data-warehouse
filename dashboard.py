from app.database.mongodb import MongoDB
from datetime import datetime

db = MongoDB.connect()

print("\n" + "█" * 60)
print("█     FINANCIAL DATA WAREHOUSE DASHBOARD     █")
print("█" * 60)

print(f"\n📅 Report Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"💾 Database: financial_dwh")
print(f"📊 MongoDB Status: ✅ Connected")

print(f"\n📈 STATISTICS:")
print(f"   • Total Assets: {db.assets.count_documents({'isDeleted': False})}")
print(f"   • Data Sources: {db.datasources.count_documents({'isValid': True})}")
print(f"   • Time Series Records: {db.timeseries.count_documents({})}")

print(f"\n🏦 ASSETS BREAKDOWN:")
for asset_class in ["stock", "crypto"]:
    count = db.assets.count_documents({"assetClass": asset_class, "isDeleted": False})
    print(f"   • {asset_class.upper()}: {count}")

print(f"\n✅ SYSTEM READY FOR DEMO")
print("█" * 60 + "\n")
