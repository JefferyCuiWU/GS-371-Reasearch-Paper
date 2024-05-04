import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Sample data: replace with your actual data
data = {
    'Date': ['3/23/2018', '3/23/2018', '7/6/2018', '8/23/2018', '6/1/2019', '6/1/2019', 
             '6/1/2019', '6/1/2019', '2/15/2020', '2/15/2020'],
    'Category': ['Meat', 'Agricultural products, Metals, Chemicals', 'Agricultural products, Automobiles, Chemicals, Medical Equipment, Energy Products',
                 'Agricultural products, Automobiles, Chemicals, Metals', 'Metals, Machinery', 'Electronic Components, Machinery',
                 'Automobiles, Medical Equipment', 'Textiles and Apparel, Footwear', 'Agricultural products, Textiles and Apparel, Metals, Automobiles, Tools and Cutlery',
                 'Chemicals, Seeds, Furniture'],
    'Additional Tariff': ['25%', '15%', '25%', '25%', '25%', '20%', '10%', '5%', '10%', '5%']
}

df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'])

# Group by Date and create a 'Wave' label
df['Wave'] = df.groupby('Date').ngroup() + 1
df_wave = df.drop_duplicates(subset=['Date'])

# Plotting
fig, ax = plt.subplots(figsize=(20, 2))
ax.set(title="Timeline of Retaliatory Tariffs")

# Ensure timeline starts from 2018 and ends with some padding
ax.set_xlim(pd.Timestamp('2018-01-01'), df['Date'].max() + pd.DateOffset(months=6))

# Draw dots for each unique date
for date, wave in zip(df_wave['Date'], df_wave['Wave']):
    ax.plot(date, 1, 'ro')  # 'ro' stands for red dot
    ax.text(date, 1.05, f'Wave {wave}', horizontalalignment='right', rotation=45)

# Set the formatter for the date to appear on the x-axis
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonthday=15))  # Mid-month for better spacing
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.xaxis.set_minor_formatter(mdates.DateFormatter('%m'))  # Only show month on the minor ticks

# Enhance the display
plt.grid(True, which='major', linestyle='--', linewidth='0.5', color='grey')
plt.grid(True, which='minor', linestyle=':', linewidth='0.5', color='grey')
ax.yaxis.set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()  # Adjust the layout to make room for label text

# Show the plot
plt.show()
