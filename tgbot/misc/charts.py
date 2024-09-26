import io
import logging
import os
from enum import Enum

import pandas as pd
import seaborn as sns
from aiogram.types import FSInputFile, Message
from matplotlib import pyplot as plt


class ChartType(Enum):
    BAR = "bar"
    HIST = "hist"


async def send_chart(
    message: Message,
    data: dict,
    chart_type: ChartType,
    x_legend: str | None = None,
    y_legend: str | None = None,
    title: str | None = None,
) -> Message:
    if chart_type == ChartType.BAR:
        ax = prepare_bar_chart(data, x_legend, y_legend, title)
    elif chart_type == ChartType.HIST:
        ax = prepare_hist_chart(data, x_legend, title)
    else:
        raise ValueError(f"Unknown chart type: {chart_type}")
    try:
        buffer = io.BytesIO()
        fig = ax.get_figure()
        fig.savefig(buffer, format="png")
        buffer.seek(0)
        temp_file = "temp.png"
        with open(temp_file, "wb") as f:
            f.write(buffer.read())
        file = FSInputFile(temp_file)
    except ValueError as ve:
        logging.error(ve)
        return await message.answer("Error creating chart. Try again later.")
    except Exception as e:
        logging.error(e)
        return await message.answer("Unexpected error. Try again later.")
    try:
        return await message.answer_photo(file)
    finally:
        os.remove(temp_file)


def prepare_hist_chart(data: dict, x_legend: str, title: str):
    sample_data = pd.DataFrame({x_legend: tuple(data[x_legend])})
    plt.clf()
    plt.xticks([1, 2, 3, 4, 5])
    ax = sns.histplot(x=x_legend, data=sample_data)
    ax.title.set_text(title)
    return ax


def prepare_bar_chart(data: dict, x_legend: str, y_legend: str, title: str):
    sample_data = pd.DataFrame(
        {
            x_legend: tuple(data[x_legend]),
            y_legend: tuple(data[y_legend]),
        }
    )
    plt.clf()
    ax = sns.barplot(x=x_legend, y=y_legend, data=sample_data)
    ax.title.set_text(title)
    return ax
