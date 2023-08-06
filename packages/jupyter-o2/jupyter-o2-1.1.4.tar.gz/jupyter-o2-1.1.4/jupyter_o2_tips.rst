===============
Jupyter-O2 tips
===============

--------------------------------------------------------------------------------------------------------------------
Troubleshooting
--------------------------------------------------------------------------------------------------------------------

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
X11 error / missing DISPLAY variable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you see ``srun: error: x11: no local DISPLAY defined``,
``No DISPLAY variable set``, or similar, you probably need to
install or reinstall `XQuartz <https://www.xquartz.org/>`__.

To test outside of Jupyter-O2, log in to the server with ``ssh -X``
and check your DISPLAY using ``echo $DISPLAY``.
There should be a string printed in response.

A possible alternative is to run Jupyter-O2 with the
``-Y`` argument to enable trusted X11 forwarding (less secure).

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
SSH error: pxssh error: could not synchronize with original prompt
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you are not on the HMS network or using the HMS VPN,
you will need to tell Jupyter-O2 use two-factor authentication
with the arguments ``--2fa --2fa-code 1``.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
nbsignatures.db
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If Jupyter hangs when opening notebooks for the first time in any
session, and the console shows error messages such as:

.. code-block::

    > The signatures database cannot be opened; maybe it is corrupted or encrypted.
    > Failed commiting signatures database to disk.

Disabling Jupyter's signatures database may be the best option, since there is
no non-networked file system shared between all the interactive compute
nodes.

1. Enter an interactive session and generate a notebook config using
   ``jupyter notebook --generate-config``
2. In ``~/.jupyter/jupyter_notebook_config.py`` set
   ``c.NotebookNotary.db_file = ':memory:'``

--------------------------------------------------------------------------------------------------------------------
Run on Windows using WSL2
--------------------------------------------------------------------------------------------------------------------

*Note: the X server installation may not be necessary, and
you can first try skipping steps 2 and 6.*

1. Install WSL2 (e.g. Ubuntu on the Windows Store)
2. Install an X server and configure WSL2 to use the X server
   (see the `Ubuntu wiki <https://wiki.ubuntu.com/WSL#Running_Graphical_Applications>`_).
   `Cygwin/X <https://x.cygwin.com>`_ is one option.
3. Add these lines to your `~/.bashrc` in WSL2, then run ``source ~/.bashrc``

.. code-block:: bash

    export DISPLAY=$(awk '/nameserver / {print $2; exit}' /etc/resolv.conf 2>/dev/null):0
    export LIBGL_ALWAYS_INDIRECT=1

4. Install Jupyter-O2 on WSL2: ``pip install jupyter-o2``
5. Configure Jupyter-O2: run ``jupyter-o2 --generate-config`` and edit the file

Now that everything is set up, run Jupyter-O2:

6. Start the X server. For Cygwin, open the Cygwin terminal and run ``startxwin``
7. Run Jupyter-O2, e.g. ``jupyter-o2 notebook``

--------------------------------------------------------------------------------------------------------------------
Useful Jupyter add-ons
--------------------------------------------------------------------------------------------------------------------

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
`Kernels <https://github.com/jupyter/jupyter/wiki/Jupyter-kernels>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are many kernels available for Jupyter, allowing the user to write
notebooks in their desired language.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
`bash_kernel <https://pypi.python.org/pypi/bash_kernel>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since Jupyter-O2 runs Jupyter on an interactive node, bash notebooks
can be used to document your session on O2, including commands and
outputs, without using SLURM to submit additional jobs.

``%%bash`` can be used to run a ``bash`` command in the default kernel,
but it does not remember your working directory or other variables
from previous cells.

Just be sure that your node has sufficient memory for the desired tasks,
or you could find your notebook server shutting down unexpectedly. SLURM
jobs can also be submitted and monitored from within a notebook to avoid
this issue.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
`jupyter contrib nbextensions <https://github.com/ipython-contrib/jupyter_contrib_nbextensions>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

jupyter contrib nbextensions adds a useful nbextensions configuration
tab to the main jupyter site. It also includes many useful extensions.

~~~~~~~~~~~~~~~~~~~~~~~~~~~
AutoSaveTime (recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Set the auto-save time to 2 minutes to reduce the risk of losing changes
due to a lost connection or closure of the interactive node.
For example, the connection could time out or the node could exceed its time limit.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
`JupyterLab <https://github.com/jupyterlab/jupyterlab>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

JupyterLab is now
`ready for users <https://blog.jupyter.org/jupyterlab-is-ready-for-users-5a6f039b8906>`__.

JupyterLab offers a more complete environment than Jupyter Notebook.
With tabs for notebooks, terminals, consoles, text editors, and an integrated file browser,
you could run almost anything you need on O2 from a single browser window.
