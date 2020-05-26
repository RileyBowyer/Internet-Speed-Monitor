import speedtest
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.ticker as ticker
import argparse
import datetime as dt
import csv
import numpy as np

download = []
upload = []
time = []

# This function is called periodically from FuncAnimation
def animate(i, st, download, upload, time, ax1, ax2):

    # Add x and y to lists
    time.append(dt.datetime.now().strftime("%d/%m/%y %H:%M:%S"))
    download.append(st.download()/1e6)
    upload.append(st.upload()/1e6)

    # Draw x and y lists
    ax1.clear()
    ax1.plot(time, download)
    ax2.clear()
    ax2.plot(time, upload)

    # Format plot
    ax1.set_xticks([])
    ax1.yaxis.set_major_locator(ticker.AutoLocator())
    ax1.yaxis.set_minor_locator(ticker.AutoMinorLocator())

    ax2.xaxis.set_major_locator(ticker.AutoLocator())
    ax2.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax2.yaxis.set_major_locator(ticker.AutoLocator())
    ax2.yaxis.set_minor_locator(ticker.AutoMinorLocator())

    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    ax1.set_title("Download Speed")
    ax2.set_title("Upload Speed")
    ax1.set_ylabel("Speed (Mb/s")
    ax2.set_ylabel("Speed (Mb/s")
    ax2.set_xlabel("Time")
    plt.tight_layout()
    


# Set up plot to call animate() function periodically



def main():
    parser = argparse.ArgumentParser(description='Internet Speed Monitor.')
    parser.add_argument('-f', type=float,
                    help='Test Interval in seconds.')

    args = parser.parse_args()
    if args.f == None:
        print("Please enter a valid frequency.")
        parser.print_help()
        return
    frequency = args.f * 1000
    st = speedtest.Speedtest() 

    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1)
    ax1.margins(0.3)
    ax2 = fig.add_subplot(2, 1, 2)
    ax2.margins(0.3)
    
    ani = animation.FuncAnimation(fig, animate, fargs=(st, download, upload, time, ax1, ax2), interval=frequency)
    plt.style.use('fivethirtyeight')
    plt.show()

if __name__ == "__main__":
    try:
        main()
        while True: pass
    except KeyboardInterrupt:
        output = []
        for index in range(len(time)):
            output.append([time[index],download[index],upload[index]])
        with open('speed.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(output)


