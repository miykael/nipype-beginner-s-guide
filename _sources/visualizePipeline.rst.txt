===========================
How To Visualize A Pipeline
===========================

The option to visualize your workflow is a great feature of Nipype. It allows you to see your analysis in one piece, control the connections between the nodes and check which input and output fields are connected.


What kind of graph do you need?
===============================

You can visualize your pipeline as soon as you have a workflow that contains any nodes and connections between them. To create a graph, simply use the function ``write_graph()`` on your workflow:

.. code-block:: py

   workflow.write_graph(graph2use='flat')

Nipype can create five different kinds of graphs by setting the variable ``graph2use`` to the following parameters:

* ``orig`` shows only the main workflows and omits any subworkflows
* ``flat`` shows all workflows, including any subworkflows
* ``exec`` shows all workflows, including subworkflows and expands iterables into subgraphs
* ``hierarchical`` shows all workflows, including subworkflows and also shows the hierarchical structure
* ``colored`` gives you the same output as ``hierarchical`` but color codes the different levels and the connections within those levels according to their hierarchical depth.

All types, except hierarchical and colored, create two graph files. The difference of those two files is in the level of detail they show. There is a **simple overview graph** called ``graph.dot`` which gives you the basic connections between nodes and a **more detailed overview graph** called ``graph_detailed.dot`` which additionally gives you the output and input fields of each node and the connections between them. The **hierarchical** and **colored graph** on the other side create only a simple overview graph. I mostly use **colored** graphs, as it gives you a fast and clear picture of your workflow structure.

.. note::
   The ``graph`` files can be found in the highest pipeline folder of your working directory.

   If graphviz is installed the dot files will automatically be converted into png-files. If not, take and load the dot files in any graphviz visualizer of your choice.


Tweak your visualization
========================

There are two additional parameters ``format`` and ``simple_form`` that you can use to change your output graph. ``format`` can be used to change the output format of the image file to either ``png`` or ``svg``. ``simple_form`` determines if the node name shown in the visualization is either of the form ``nodename (package)`` when set to ``True`` or ``nodename.Class.package`` when set to ``False``.

.. code-block:: py

   workflow.write_graph(graph2use='colored', format='svg', simple_form=True)

To illustrate, on the left you can see a simple graph of the visualization type **orig** when ``simple_form`` is set to ``True`` and on the right if it is set to ``False``.


.. only:: html

    .. image:: images/graph_orig_simple.svg
       :height: 250pt

    .. image:: images/graph_orig_notsimple.svg
       :height: 250pt


.. only:: latex

    .. image:: images/graph_orig_simple.png
       :height: 150pt

    .. image:: images/graph_orig_notsimple.png
       :height: 200pt


Examples of each visualization type
===================================

The graphs shown below are visualizations of the **first level analysis pipeline** or ``metaflow`` from the section: `How To Build A First Level Pipeline <http://miykael.github.io/nipype-beginner-s-guide/firstLevel.html>`_


``orig`` - simple graph
~~~~~~~~~~~~~~~~~~~~~~~

The simple graph of the visualization type ``orig`` shows only the top layer, i.e. hierarchical highest workflows and nodes, of your workflow. In this case this is the ``metaflow``. Subworkflows such as ``preproc`` and ``l1analysis1`` are represented by a single node.

.. only:: html

    .. image:: images/graph_orig_simple.svg
       :align: center
       :width: 300pt

.. only:: latex

    .. image:: images/graph_orig_simple.png
       :align: center
       :width: 180pt


``orig`` - detailed graph
~~~~~~~~~~~~~~~~~~~~~~~~~

The detailed graph of the visualization type ``orig`` shows the ``metaflow`` to the same depth as the simple version above, but with a bit more information about input and output fields. Now you can see which output of which node is connected to which input of the following node.

.. only:: html

    .. image:: images/graph_orig_detailed.svg
       :align: center
       :width: 600pt

.. only:: latex

    .. image:: images/graph_orig_detailed.png
       :align: center
       :width: 465pt


``flat`` - simple graph
~~~~~~~~~~~~~~~~~~~~~~~

The simple graph of the visualization type ``flat`` shows all nodes of a workflow. As you can see, subworkflows such as ``preproc`` and ``l1analysis1`` are now expanded and represented by all their containing nodes.

.. only:: html

    .. image:: images/graph_flat_simple.svg
       :align: center
       :width: 600pt

.. only:: latex

    .. image:: images/graph_flat_simple.png
       :align: center
       :width: 450pt


``flat`` - detailed graph
~~~~~~~~~~~~~~~~~~~~~~~~~

The detailed graph of the visualization type ``flat`` shows the ``metaflow`` in all its glory. This graph shows all nodes, their inputs and outputs and how they are connected to each other.

.. only:: html

    .. image:: images/graph_flat_detailed.svg
       :align: center
       :width: 600pt

.. only:: latex

    .. image:: images/graph_flat_detailed.png
       :align: center
       :width: 450pt


``exec`` - simple graph
~~~~~~~~~~~~~~~~~~~~~~~

The detailed graph of the visualization type ``exec`` doesn't really show you anything different than the simple graph of the visualization type ``flat``. The advantage of the ``exec`` type lies in the detailed graph.

.. only:: html

    .. image:: images/graph_exec_simple.svg
       :align: center
       :width: 600pt

.. only:: latex

    .. image:: images/graph_exec_simple.png
       :align: center
       :width: 465pt


``exec`` - detailed graph
~~~~~~~~~~~~~~~~~~~~~~~~~

The detailed graph of the visualization type ``exec`` shows you the nodes of the ``metaflow`` with the same details as the visualization type ``flat`` would do. But additionally, all iterables are expanded so that you can see the full hierarchical and parallel structure of your analysis. In the following example the node ``selectfiles`` iterates over ``sub001``, ``sub002`` and ``sub003``.

.. only:: html

    .. image:: images/graph_exec_detailed.svg
       :align: center
       :width: 600pt

.. only:: latex

    .. image:: images/graph_exec_detailed.png
       :align: center
       :width: 465pt


.. note::

   As you can see from this example, every iteration creates a subgraph with its own index. In this case ``a0``, ``a1`` and ``a2``. Such an indexing structure is also maintained in the folders and subfolders of your working and output directory.


``hierarchical`` - simple graph
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The graph of the visualization type ``hierarchical`` shows the ``metaflow`` as seen with the visualization type ``flat`` but emphasizes the hierarchical structure of its subworkflows. This is done by surrounding each subworkflow with a box labeled with the name of the subworkflow. Additionally, each node with an iterable field will be shown as a gray box.

.. only:: html

    .. image:: images/graph_hierarchical.svg
       :align: center
       :width: 600pt

.. only:: latex

    .. image:: images/graph_hierarchical.png
       :align: center
       :width: 450pt


In this example you see that the ``metaflow`` contains a ``preproc`` and a ``l1analysis`` workflow.


``colored`` - simple graph
~~~~~~~~~~~~~~~~~~~~~~~~~~

The graph of the visualization type ``colored`` shows the ``metaflow`` as seen with the visualization type ``hierarchical`` but color codes the different ``hierarchical`` levels as well as the connections between and within those levels with different colors.

.. only:: html

    .. image:: images/graph_colored.svg
       :align: center
       :width: 600pt

.. only:: latex

    .. image:: images/graph_colored.png
       :align: center
       :width: 450pt
