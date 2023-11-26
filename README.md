# Introduction
This script smooths geometry.

The primary use is to smooth geometry from inside the script rather than having to rely on an external Smoothing deformer or anything of the sorts. It is controllable by changing a parameter in the function call.

The script can easily be ported to other software and languages.

For each point the algorithm gets the average of all connected points. Apply stiffness, repeat by steps.

![image](https://github.com/YoYoFreakCJ/C4D-Smooth/assets/59722190/d1b24118-fd41-40dd-a4e3-7a810a20f3e7)

# Usage
Paste the two functions from Smooth.py into your script. You need a variable holding the geometry to smooth, then simply call:

```py
smooth_points(poly_obj)
```

Parameters:

|Name|Type|Description|Default|
|--|--|--|--|
|poly_obj|c4d.PolygonObject|The polygon object to smooth.|
|steps|int|*Optional* - The number of smoothing iterations.|1|
|stiffness|float|*Optional* - The stiffness of the model. Use this to adjust the smoothing strength.|0.5|
|points_indices_to_smooth|list[int]|*Optional* - The indices of the points to smooth. Pass None or an empty array to smooth everything.|[]|
|neighbor|c4d.utils.Neighbor|*Optional* - The Neighbor object used to identify connected vertices. If None is passed it will be created and initialized in the function.|None|

See Sample.py for a complete sample.

# Disclaimer

Tested on Cinema 4D 2024.1.0.

Use at your own risk, I'm not liable for any damages this may cause.
