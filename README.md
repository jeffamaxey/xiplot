# &chi;iplot

&chi;iplot, pronounced like "kaiplot"[^1], is a web-first visualisation platform for multidimensional data, implemented in the `xiplot` Python package.

[^1]: Pronouncing &chi;iplot like "xaiplot" is also recognised.

## Description

&chi;iplot is built on top of ![Dash Framework](https://github.com/plotly/dash) with its various extensions (see the ![requirements.txt](https://github.com/edahelsinki/xiplot/blob/main/requirements.txt)). The goal of the &chi;iplot is to explore new insights from the collected data and to make data exploring user-friendly and intuitive.

&chi;iplot can be executed in server version or WASM-based browser version. 

## Dependencies

Install the depencies by running `pip install -r requirements.txt`

## Execution

### Server version

Run `python3 -m xiplot` at the root directory.

### Browser version

[https://www.edahelsinki.fi/xiplot](https://www.edahelsinki.fi/xiplot)

## Dataframe loading and saving

`xiplot` uses `pandas` to load dataframes from `.csv`, `.json`, `.pkl`, and &ndash; if `feather-format` is available &ndash; `.ft` files. If you are running `xiplot` locally, you can simply copy your datasets into the `data/` folder. If you are accessing `xiplot` remotely or you do not want to pollute the `data/` folder, you can upload the dataset into memory directly inside `xiplot`: navigate to the data tab and either click the upload button to the right or drag the file into it.

To save the currently loaded dataset, you can navigate to the data tab and press the "Download only the data file" button. The downloaded file will contain the unmodified content of the original dataset.

## Plot saving and loading

`xiplot` also supports saving the plots you have created in combination with the data it was generated with. To download a `.tar` archive containing the original dataset, auxiliary columns generated by `xiplot`, and the settings of all plots, navigate to the data tab and press the "Download the combined plots-and-data file" button.

You can also resume working on a previously saved plots-and-data file by uploading it, just like a dataframe as described above, using the upload button in the data tab. Once the data itself is loaded, all plots will be recreated. Note that if any plot recreation fails, you will receive an error message popup, but `xiplot` will still attempt to recreate the other plots as well.

### The combined plots-and-data file format

If you download a combined plots-and-data file from `xiplot`, you will receive a `.tar` file, whose format you must follow if you want to generate your own to plots-and-data file to upload.

The combined plots-and-data file has a filename `DATASET.tar`, where `DATASET` is a name of your choosing. Inside this tar archive, at the root level, are exactly the following three files, i.e. no other files or folders:

- `data.EXT` where `EXT` is one of the following extensions: `csv|json|pkl|ft`
- `aux.EXT`
- `meta.json`

The `data.EXT` file contains the dataset dataframe that will be loaded using `read_csv`, `read_json`, `read_pickle`, or `read_feather`. Note that when reading a json file, `xiplot` tries reading the dataset both in columns (`pd.read_json(file, typ="frame", orient="columns")`) and split (`pd.read_json(file, typ="frame", orient="split")`) mode.

The `aux.EXT` file contains auxiliary columns for the dataset. It is stored in the same file format as the dataset dataframe. It must either be empty, or have the same number of rows as the dataset dataframe.

The `meta.json` file contains metadata that describe the state of `xiplot` upon saving, including the settings for all created plots. It follows the following (loose) json schema, where programmatic interpolations are marked by comments and `VARIABLES`:

```json
{
    "type": "object",
    "properties": {
        "filename": {
            // filename should equal "DATASET.EXT"
            "type": "string"
        },
        "settings": {
            "type": "object",
            "properties": {
                "cluster-tab": {
                    "type": "object",
                    "properties": {
                        "selection": {
                            "type": "object",
                            "properties": {
                                "mode": {
                                    // Selecting clusters in fg-bg mode marks
                                    //  the selection as c1 and the rest as c2
                                    // Selecting clusters in draw mode marks
                                    //  the selection according to the brush
                                    // By default fg-bg is chosen
                                    "enum": ["fg-bg", "draw"]
                                },
                                "brush": {
                                    // brush is required if mode="draw"
                                    "enum": CLUSTER_CLASSES,
                                }
                            },
                            "if": {
                                "properties": {
                                    "mode": {
                                        "const": "draw"
                                    }
                                }
                            },
                            "then": {
                                "required": ["brush"]
                            }
                        }
                    }
                }
            }
        },
        "plots": {
            "type": "object",
            "patternProperties": {
                // Each plot is assigned a unique uuid, e.g. using uuidv4
                "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$": {
                    // The plot settings object is specialised by every plot type
                    "type": "object",
                    "properties": {
                        "type": {
                            "enum": PLOT_TYPES,
                            ...PLOT_SETTINGS,
                        },
                    },
                    "required": ["type"]
                }
            },
            "additionalProperties": false
        }
    },
    "required": ["filename", "settings", "plots"]
}
```

where `CLUSTER_CLASSES` is defined as (`"all"` is a special class that every datapoint is implicitly assigned to):
```json
["all", "c1", ..., "c9"]
```

and where `PLOT_TYPES` is the list of plot type names registered with `xiplot`, with `PLOT_SETTINGS` being the additional properties defined for that plot type. At present, `xiplot` defines the following plot types, which define their respective plot settings objects:

#### Scatterplot

```json
{
    "type": "object",
    "properties": {
        "type": {
            "const": "Scatterplot"
        },
        "axes": {
            "type": "object",
            "properties": {
                "x": {
                    // By default, a numeric column name starting with 'x-'
                    //  or containing ' 1' or the first one is chosen
                    "enum": NUMERIC_COLUMN_NAMES
                },
                "y": {
                    // By default, a numeric column name starting with 'y-'
                    //  or containing ' 2' or the second one is chosen
                    "enum": NUMERIC_COLUMN_NAMES
                }
            }
        },
        "colour": {
            // By default, 'Clusters' is chosen
            "enum": [...COLUMN_NAMES, null]
        },
        "symbol": {
            // By defauly, null is chosen
            "enum": [...COLUMN_NAMES, null]
        },
        "jitter": {
            // By default, 0.0 is chosen
            "type": "number",
            "minimum": 0.0
        }
    }
}
```

#### Histogram

```json
{
    "type": "object",
    "properties": {
        "type": {
            "const": "Histogram"
        },
        "axes": {
            "type": "object",
            "properties": {
                "x": {
                    // By default, a numeric column name starting with 'x-'
                    //  or containing ' 1' or the first one is chosen
                    "enum": NUMERIC_COLUMN_NAMES
                }
            }
        },
        "groupby": {
            // By default, implicitly "Clusters", unless classes is specified
            "enum": ["Clusters"]
        },
        "classes": {
            // By default, the empty list [], unless groupby is specified
            "type": "array",
            "items": {
                "enum": CLUSTER_CLASSES
            },
            "uniqueItems": true
        }
    },
    "dependentRequired": {
        "classes": ["groupby"],
        "groupby": ["classes"],
    }
}
```

#### Heatmap

```json
{
    "type": "object",
    "properties": {
        "type": {
            "const": "Heatmap"
        },
        "clusters": {
            "type": "object",
            "properties": {
                "amount": {
                    // By default, 2 is chosen
                    "type": "integer",
                    "minimum": 2,
                    "maximum": 10
                }
            }
        }
    }
}
```

#### Barplot

```json
{
    "type": "object",
    "properties": {
        "type": {
            "const": "Barplot"
        },
        "axes": {
            "type": "object",
            "properties": {
                "x": {
                    // By default, the first integer or string-iterable
                    //  column name is chosen
                    "enum": INTEGER_OR_STR_ITERABLE_COLUMN_NAMES
                },
                "y": {
                    // By default, "frequency" is chosen
                    "enum": ["frequency", ...NUMERIC_COLUMN_NAMES]
                }
            }
        },
        "groupby": {
            // By default, implicitly "Clusters", unless classes is specified
            "enum": ["Clusters"]
        },
        "classes": {
            // By default, the empty list [], unless groupby is specified
            "type": "array",
            "items": {
                "enum": CLUSTER_CLASSES
            },
            "uniqueItems": true
        },
        "order": {
            // In reldiff mode, the bar groups are sorted by their maxium
            //  inter-class difference
            // In total mode, the bar groups are sorted by their sum totals
            // By default, the reldiff mode is chosen
            "enum": ["reldiff", "total"]
        }
    },
    "dependentRequired": {
        "classes": ["groupby"],
        "groupby": ["classes"],
    }
}
```

#### Table

```json
{
    "type": "object",
    "properties": {
        "type": {
            "const": "Table"
        },
        "columns": {
            "type": "object",
            "properties": {
                // Every column name in the dataset and "Clusters" can be used
                COLUMN_NAME: {
                    "type": "object",
                    "properties": {
                        "hidden": {
                            // Hidden columns are still loaded and can be used
                            //  for sorting and filtering
                            // By default, false is used
                            "type": "boolean"
                        },
                        "sorting": {
                            // Not including the sorting means the column is
                            //  the table is NOT sorted by this column
                            "enum": ["asc", "desc"]
                        }
                    }
                }
            }
        },
        "query": {
            // The filter query for the table uses plotly dash's filter_query
            //  syntax: https://dash.plotly.com/datatable/filtering
            // By default, no filter query is used
            "type": "string"
        },
        "page": {
            "type": "integer",
            "minimum": 0
        }
    }
}
```

#### Smiles

```json
{
    "type": "object",
    "properties": {
        "type": {
            "const": "Smiles"
        },
        "clusters": {
            "type": "object",
            "properties": {
                "mode": {
                    // In hover mode, the smiles string is changed when hovering
                    //  over a data point with a smiles column
                    // In click mode, the smiles string is changed when clicking
                    //  a data point with a smiles column
                    // In lock mode, the smiles string is locked
                    "enum": ["hover", "click", "lock"]
                },
                "smiles": {
                    "type": "string"
                }
            }
        }
    }
}
```
