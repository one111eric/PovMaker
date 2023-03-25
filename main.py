import gradio as gr
import PovMaker
import time


def generate(src, scn, ss, ref, out,progress=gr.Progress(track_tqdm=True)):
    newPovMaker = PovMaker.PovMaker(src,scn,ss,ref,out)

    progress(0, desc="Starting")
    start = time.time()
    newPovMaker.split()
    newPovMaker.match()
    newPovMaker.merge()
    end = time.time()
    return "Finished in " + str(end-start) + " seconds"



with gr.Blocks() as demo:
    gr.HTML(value="<h1>POV Maker</h1>")
    with gr.Row():
        with gr.Column():
            sourceFolder = gr.Textbox(
                label="Source Folder", elem_id="source_folder")
            # sourceFolderPicker = gr.File(file_count="directory")
        with gr.Column():
            sceneFolder = gr.Textbox(
                label="Scenes Folder", elem_id="scenes_folder")
        with gr.Column():
            ssFolder = gr.Textbox(
                label="Screenshot Folder", elem_id="screenshot_folder")
        with gr.Column():
            refFolder = gr.Textbox(
                label="Reference Folder", elem_id="ref_folder")
        with gr.Column():
            outputFolder = gr.Textbox(
                label="Output Folder", elem_id="output_folder")
    with gr.Row():
        result = gr.Textbox(label="result", elem_id="result")
    btn = gr.Button("Run")
    btn.click(fn=generate, inputs=[sourceFolder,
              sceneFolder, ssFolder, refFolder, outputFolder], outputs=result)
demo.queue()
demo.launch()
