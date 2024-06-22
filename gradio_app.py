import os

from pathlib import Path

import gradio as gr

import asyncio

import pandas as pd
from asyncflows import AsyncFlows
from asyncflows.utils.async_utils import merge_iterators

from asyncflows.log_config import get_logger


with gr.Blocks() as demo:
    query = gr.Textbox(label="What is your problem?Please...", placeholder="Provide a problem to think about")
    submit_button = gr.Button("Submit")

    with gr.Row():
        white_hat = gr.Textbox(label="White Hat", interactive=False)
        red_hat = gr.Textbox(label="Red Hat", interactive=False)
        black_hat = gr.Textbox(label="Black Hat", interactive=False)
        yellow_hat = gr.Textbox(label="Yellow Hat", interactive=False)
        green_hat = gr.Textbox(label="Green Hat", interactive=False)
        my_hat = gr.Textbox(label="My Hat", interactive=False)
    blue_hat = gr.Textbox(label="Blue Hat (synthesis)", interactive=False)

    async def handle_submit(query):
        # Clear the output fields
        yield {
            white_hat: "",
            red_hat: "",
            black_hat: "",
            yellow_hat: "",
            green_hat: "",
            my_hat: "",
            blue_hat: "",
        }

        # Load the chatbot flow
        flow = AsyncFlows.from_file("debono.yaml").set_vars(
            query=query,
        )

        log = get_logger()

        # Stream the hats
        async for hat, outputs in merge_iterators(
            log,
            [
                white_hat,
                red_hat,
                black_hat,
                yellow_hat,
                green_hat
            ],
            [
                flow.stream('white_hat.result'),
                flow.stream('red_hat.result'),
                flow.stream('black_hat.result'),
                flow.stream('yellow_hat.result'),
                flow.stream('green_hat.result'),
            ],
        ):
            yield {
                hat: outputs
            }

        # Stream the blue hat
        async for outputs in flow.stream("blue_hat.result"):
            yield {
                blue_hat: outputs
            }


    submit_button.click(
        fn=handle_submit,
        inputs=[query],
        outputs=[
            white_hat,
            red_hat,
            black_hat,
            yellow_hat,
            green_hat,
            blue_hat
        ],
    )


if __name__ == "__main__":
    demo.launch()
