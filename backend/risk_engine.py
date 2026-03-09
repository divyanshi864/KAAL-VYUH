def classify_risk(df):

    def risk_level(alt):
        if alt < 500:
            return "High"
        elif alt < 1000:
            return "Medium"
        else:
            return "Low"

    df["Risk"] = df["Altitude"].apply(risk_level)
    return df