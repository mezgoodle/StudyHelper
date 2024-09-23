import io
import os

import pandas as pd
import seaborn as sns
from aiogram.types import FSInputFile, Message


async def send_chart(
    message: Message,
    data,
    x_legend: str,
    y_legend: str,
    title: str | None = None,
) -> Message:
    sample_data = pd.DataFrame(
        {
            x_legend: tuple(data[x_legend]),
            y_legend: tuple(data[y_legend]),
        }
    )
    print(sample_data)
    ax = sns.barplot(x=x_legend, y=y_legend, data=sample_data)
    ax.title.set_text(title)
    buffer = io.BytesIO()
    fig = ax.get_figure()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    temp_file = "temp.png"
    with open(temp_file, "wb") as f:
        f.write(buffer.read())

    file = FSInputFile(temp_file, filename="my_graph.png")
    try:
        return await message.answer_photo(file)
    finally:
        os.remove(temp_file)
