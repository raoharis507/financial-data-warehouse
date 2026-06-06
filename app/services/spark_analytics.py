from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col, row_number, desc
from pyspark.sql.window import Window
from pyspark.ml.regression import LinearRegression
from pyspark.ml.feature import VectorAssembler
from app.database.mongodb import MongoDB
import pandas as pd

class SparkAnalyticsService:
    _spark = None
    
    @classmethod
    def get_spark(cls):
        if cls._spark is None:
            cls._spark = SparkSession.builder \
                .appName("FinancialDataWarehouse") \
                .config("spark.sql.adaptive.enabled", "true") \
                .master("local[*]") \
                .getOrCreate()
        return cls._spark
    
    @classmethod
    async def calculate_moving_average_spark(cls, asset_id: str, provider: str, days: int = 5):
        """Calculate moving average using Spark SQL"""
        try:
            spark = cls.get_spark()
            db = MongoDB.get_db()
            
            # Fetch data from MongoDB
            data = list(db.timeseries.find(
                {"assetId": asset_id, "provider": provider},
                {"_id": 0, "timestamp": 1, "closePrice": 1}
            ).sort("timestamp", -1).limit(days * 2))
            
            if len(data) < 2:
                return {"error": "Insufficient data"}
            
            # Convert to Spark DataFrame
            pdf = pd.DataFrame(data)
            df = spark.createDataFrame(pdf)
            
            # Create window specification
            windowSpec = Window.orderBy(desc("timestamp")).rowsBetween(0, days-1)
            
            # Calculate moving average
            result_df = df.withColumn("moving_avg", avg("closePrice").over(windowSpec))
            result = result_df.select("moving_avg").first()
            
            ma_value = float(result[0]) if result else 0
            
            return {
                "assetId": asset_id,
                "period_days": days,
                "moving_average": round(ma_value, 2),
                "engine": "Apache Spark"
            }
        except Exception as e:
            return {"error": str(e), "engine": "Apache Spark"}
    
    @classmethod
    async def forecast_price_spark(cls, asset_id: str, provider: str, days_ahead: int = 3):
        """Price forecast using Spark MLlib Linear Regression"""
        try:
            spark = cls.get_spark()
            db = MongoDB.get_db()
            
            # Fetch historical data
            data = list(db.timeseries.find(
                {"assetId": asset_id, "provider": provider},
                {"_id": 0, "timestamp": 1, "closePrice": 1}
            ).sort("timestamp", 1).limit(30))
            
            if len(data) < 3:
                return {"error": "Need at least 3 data points"}
            
            # Create DataFrame with numeric time index
            pdf = pd.DataFrame(data)
            pdf['time_index'] = list(range(len(pdf)))
            df = spark.createDataFrame(pdf)
            
            # Prepare features using VectorAssembler (Spark ML)
            assembler = VectorAssembler(inputCols=["time_index"], outputCol="features")
            df_features = assembler.transform(df)
            
            # Train Linear Regression model using Spark MLlib
            lr = LinearRegression(featuresCol="features", labelCol="closePrice")
            model = lr.fit(df_features)
            
            # Make predictions
            future_indices = [(len(data) + i) for i in range(days_ahead)]
            future_df = spark.createDataFrame(pd.DataFrame({'time_index': future_indices}))
            future_features = assembler.transform(future_df)
            predictions = model.transform(future_features)
            
            pred_values = [row.prediction for row in predictions.collect()]
            
            return {
                "assetId": asset_id,
                "forecast_days": days_ahead,
                "predictions": [round(p, 2) for p in pred_values],
                "trend": "up" if model.coefficients[0] > 0 else "down",
                "engine": "Apache Spark MLlib"
            }
        except Exception as e:
            return {"error": str(e), "engine": "Apache Spark"}
