def generate_signal(df):
    df['SMA20'] = df['Close'].rolling(window=20).mean()
    df['Signal'] = None

    for i in range(20, len(df)):
        if df['Close'][i] > df['SMA20'][i] and df['Close'][i-1] <= df['SMA20'][i-1]:
            df.at[i, 'Signal'] = 'BUY'
        elif df['Close'][i] < df['SMA20'][i] and df['Close'][i-1] >= df['SMA20'][i-1]:
            df.at[i, 'Signal'] = 'SELL'
    
    return df
