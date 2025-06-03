import pydataprocessing as dp
import pandas as pd
import streamlit as st
import uuid

def _decode(x):
    try:
        return  x.decode()
    except:
        return x

def process(platform_base, panel_base):
    path = f"{uuid.uuid1()}"
    merge_bases(panel_base, platform_base, path)
    st.session_state.download_base = f"out/{path}.zsav"


def process_panel(panel_base):
    pdf, pmeta = dp.read_spss(panel_base)

    pdf["date_created"] = pd.to_datetime(pdf["date_created"].apply(lambda x: _decode(x)))
    pdf["date_created"] = pdf["date_created"].dt.strftime('%d.%m.%Y %H:%M:%S')

    pdf["date_modified"] = pd.to_datetime(pdf["date_modified"].apply(lambda x: _decode(x)))
    pdf["date_modified"] = pdf["date_modified"].dt.strftime('%d.%m.%Y %H:%M:%S')

    # Format to HH.MM.SS using a custom function

    pdf['survey_time'] = pdf['survey_time'].fillna(0)
    pdf['survey_time'] = pdf['survey_time'].astype(int)
    timedeltas = pd.to_timedelta(pdf['survey_time'], unit='s')

    # Format to HH.MM.SS
    pdf['survey_time'] = timedeltas.apply(
        lambda
            x: f"{int(x.total_seconds() // 3600):02}.{int((x.total_seconds() % 3600) // 60):02}.{int(x.total_seconds() % 60):02}"
    )

    pdf = pdf.rename(
        {
            "platform_name": "CollectorNM"
        },
        axis="columns",

    )
    return pdf


def process_platform(platform_base):
    df, meta = dp.read_spss(platform_base)
    meta.type_vars(df)
    return df, meta


def merge_bases(panel_base, platform_base, path):
    panel = process_panel(panel_base.getvalue())
    df, meta = process_platform(platform_base.getvalue())

    pdf_start = 9
    df_start = 7

    j = pdf_start

    mapper = {}

    with st.expander("Переписываю переменные:", expanded=False):

        for _i in range(len(df.columns) - df_start):
            i = df_start + _i
            var = df.columns[i]

            if meta.q_type[var] == "info_screen":
                continue

            if j == len(panel.columns):
                break

            pdf_var = panel.columns[j]
            mapper[pdf_var] = var

            j += 1
            st.markdown(f"{pdf_var} -> {var}")

    pdf = panel.rename(mapper, axis=1)

    cols = [col for col in pdf.columns if col in df.columns]

    fin = pd.concat(
        [df, pdf[cols]],
        axis=0
    )

    dp.write_spss(fin, meta, "out", path)