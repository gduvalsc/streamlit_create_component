from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
import tempfile, os, inspect
def showcodeandrun(bloc):
    st.code(bloc)
    compiled_code = compile(bloc, "<string>", "exec")
    exec(compiled_code)
    st.divider()

def gensimplecomponent(name, template="", script=""):
    def html():
        return f"""
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="UTF-8" />
                    <title>{name}</title>
                    <script>
                        function sendMessageToStreamlitClient(type, data) {{
                            const outData = Object.assign({{
                                isStreamlitMessage: true,
                                type: type,
                            }}, data);
                            window.parent.postMessage(outData, "*");
                        }}

                        const Streamlit = {{
                            setComponentReady: function() {{
                                sendMessageToStreamlitClient("streamlit:componentReady", {{apiVersion: 1}});
                            }},
                            setFrameHeight: function(height) {{
                                sendMessageToStreamlitClient("streamlit:setFrameHeight", {{height: height}});
                            }},
                            setComponentValue: function(value) {{
                                sendMessageToStreamlitClient("streamlit:setComponentValue", {{value: value}});
                            }},
                            RENDER_EVENT: "streamlit:render",
                            events: {{
                                addEventListener: function(type, callback) {{
                                    window.addEventListener("message", function(event) {{
                                        if (event.data.type === type) {{
                                            event.detail = event.data
                                            callback(event);
                                        }}
                                    }});
                                }}
                            }}
                        }}
                    </script>

                </head>
            <body>
            {template}
            </body>
            <script>
                {script}
            </script>
            </html>
        """

    dir = f"{tempfile.gettempdir()}/{name}"
    if not os.path.isdir(dir): os.mkdir(dir)
    fname = f'{dir}/index.html'
    f = open(fname, 'w')
    f.write(html())
    f.close()
    func = components.declare_component(name, path=str(dir))
    def f(**params):
        component_value = func(**params)
        return component_value
    return f


def gencomponent(name, template="", script=""):
    def html():
        return f"""
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="UTF-8" />
                    <title>{name}</title>
                    <link rel="stylesheet" href="https://unpkg.com/element-ui/lib/theme-chalk/index.css">
                    <script>
                        function sendMessageToStreamlitClient(type, data) {{
                            const outData = Object.assign({{
                                isStreamlitMessage: true,
                                type: type,
                            }}, data);
                            window.parent.postMessage(outData, "*");
                        }}

                        const Streamlit = {{
                            setComponentReady: function() {{
                                sendMessageToStreamlitClient("streamlit:componentReady", {{apiVersion: 1}});
                            }},
                            setFrameHeight: function(height) {{
                                sendMessageToStreamlitClient("streamlit:setFrameHeight", {{height: height}});
                            }},
                            setComponentValue: function(value) {{
                                sendMessageToStreamlitClient("streamlit:setComponentValue", {{value: value}});
                            }},
                            RENDER_EVENT: "streamlit:render",
                            events: {{
                                addEventListener: function(type, callback) {{
                                    window.addEventListener("message", function(event) {{
                                        if (event.data.type === type) {{
                                            event.detail = event.data
                                            callback(event);
                                        }}
                                    }});
                                }}
                            }}
                        }}
                    </script>

                </head>
            <body>
            {template}
            </body>
            <script src="https://unpkg.com/vue@2/dist/vue.js"></script>
            <script src="https://unpkg.com/element-ui/lib/index.js"></script>
            <script>
                {script}
            </script>
            </html>
        """

    dir = f"{tempfile.gettempdir()}/{name}"
    if not os.path.isdir(dir): os.mkdir(dir)
    fname = f'{dir}/index.html'
    f = open(fname, 'w')
    f.write(html())
    f.close()
    func = components.declare_component(name, path=str(dir))
    def f(**params):
        component_value = func(**params)
        return component_value
    return f

st.subheader('Another way to define new components in Streamlit', divider='rainbow')
st.markdown('I recently discovered **Streamlit**. Deploying an application through a *web browser* and coding it almost exclusively in **Python** in such a simple way is what I have been looking for for a long time.')
st.markdown('The core of Streamlit is already very rich with numerous widgets available to develop a wide range of applications. However, there are still some gaps, such as the ability to define dropdown menus or a tree view of a structure, and quickly, one needs to delve into **Streamlit Components** to supplement the range of available widgets.')
st.markdown("There are numerous examples of **components** developed by third parties on the Streamlit website (https://streamlit.io/components), and some may find what they're looking for there. Alternatively, Streamlit provides the opportunity to define your own **component** (https://docs.streamlit.io/library/components/create).")
st.markdown("I tried to go through the examples provided by third parties to find what I was looking for or, failing that, to create my own component using the official method described by Streamlit, but I came out of this experience feeling frustrated.")
st.markdown("Everything is complicated, poorly documented! I feel like extending Streamlit is as difficult as it is simple to use.")
st.markdown("The current trend in development is to define templates through a magic command (such as npm init) and then navigate somewhere within the generated directory structure to modify our piece of code. It's a black box, and the code we're interested in is hidden somewhere within this intricate tree in one or more files.")
st.markdown("I don't like this way of seeing things.")
st.markdown("I much prefer trying to concentrate things in one place. Anything that defines a component should be isolated within a block of lines belonging to the same file!")
st.markdown("Yes, it is possible to create sophisticated components that extend Streamlit, all while concentrating the code of these components in a single place and without creating a complex structure around them. We will try to demonstrate this using examples without leaving this thread!")
st.markdown("Another criticism: I tried to find documentation showing the architecture of Streamlit and specifically how Streamlit establishes communication between Python and the web browser. I found nothing usable. And then, after searching for a while, I discovered this thread (https://discuss.streamlit.io/t/streamlit-cookiecutter-components-template/30755), which allowed me to delve deeper into understanding the mechanisms of communication between Python and an external component.")
st.markdown("I understood that there is no direct link between Streamlit and ReactJS for developing a new component. Those who enjoy templates and frameworks like ReactJS can naturally use these environments, but it's by no means a requirement.")
st.markdown("To create a component, you simply need to create an HTML page where you define the component's rendering and enrich this page with a few lines of JavaScript. As you will see later on, the JavaScript code is very simple. It mainly consists of mechanisms to retrieve parameters from Python and transport the result from JavaScript to Python.")
st.markdown("To showcase the examples and execute them, I use the following function:")
st.code('''
def showcodeandrun(bloc):
    st.code(bloc)
    compiled_code = compile(bloc, "<string>", "exec")
    exec(compiled_code, globals())
    st.divider()
''')
st.markdown("An example:")
showcodeandrun("""
import streamlit as st
st.subheader("A subheader in action", divider="rainbow")
st.markdown("This is an **example**!")
""")
st.markdown("Alright, we are now ready to define and create our first component!")
st.markdown("Firstly, we will define a very simple component based on the HTML <input> element, and we will define what is needed for the input field's content to be usable by the Streamlit code.")
st.markdown("To define a component, we use the following function:")
st.code('''
def gensimplecomponent(name, template="", script=""):
    def html():
        return f"""
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="UTF-8" />
                    <title>{name}</title>
                    <script>
                        function sendMessageToStreamlitClient(type, data) {{
                            const outData = Object.assign({{
                                isStreamlitMessage: true,
                                type: type,
                            }}, data);
                            window.parent.postMessage(outData, "*");
                        }}

                        const Streamlit = {{
                            setComponentReady: function() {{
                                sendMessageToStreamlitClient("streamlit:componentReady", {{apiVersion: 1}});
                            }},
                            setFrameHeight: function(height) {{
                                sendMessageToStreamlitClient("streamlit:setFrameHeight", {{height: height}});
                            }},
                            setComponentValue: function(value) {{
                                sendMessageToStreamlitClient("streamlit:setComponentValue", {{value: value}});
                            }},
                            RENDER_EVENT: "streamlit:render",
                            events: {{
                                addEventListener: function(type, callback) {{
                                    window.addEventListener("message", function(event) {{
                                        if (event.data.type === type) {{
                                            event.detail = event.data
                                            callback(event);
                                        }}
                                    }});
                                }}
                            }}
                        }}
                    </script>

                </head>
            <body>
            {template}
            </body>
            <script>
                {script}
            </script>
            </html>
        """

    dir = f"{tempfile.gettempdir()}/{name}"
    if not os.path.isdir(dir): os.mkdir(dir)
    fname = f'{dir}/index.html'
    f = open(fname, 'w')
    f.write(html())
    f.close()
    func = components.declare_component(name, path=str(dir))
    def f(**params):
        component_value = func(**params)
        return component_value
    return f
''')
st.markdown("We need to define a name for the component (name parameter), a template (a piece of HTML to define the component's rendering), and a script. The result of the function is another function that allows declaring the component.")
st.markdown("Example:")
showcodeandrun('''
template="""
    <div id="root">
        <p> This is an example </p>
        <input type="text" name="text_input" id="input_box" />
    </div>
"""
script = """
    function onRender(event) {
        if (!window.rendered) {
            const {value} = event.detail.args;
            const input = document.getElementById("input_box");
            if (value) {
                input.value = value
            }
            input.onkeyup = event => Streamlit.setComponentValue(event.target.value)
            Streamlit.setFrameHeight(80)
            window.rendered = true
        }
    }

    Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
    Streamlit.setComponentReady()
"""
simplecomponent = gensimplecomponent('mysimplecomponent',template=template, script=script)
value = simplecomponent(key="aaa")
st.write(value)
''')
st.markdown("Once the component is defined, it can be reused n times as follows:")
showcodeandrun('''
template="""
    <div id="root">
        <p> This is an example </p>
        <input type="text" name="text_input" id="input_box" />
    </div>
"""
script = """
    function onRender(event) {
        if (!window.rendered) {
            const {value} = event.detail.args;
            const input = document.getElementById("input_box");
            if (value) {
                input.value = value
            }
            input.onkeyup = event => Streamlit.setComponentValue(event.target.value)
            Streamlit.setFrameHeight(80)
            window.rendered = true
        }
    }

    Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
    Streamlit.setComponentReady()
"""
simplecomponent = gensimplecomponent('mysimplecomponent',template=template, script=script)
value1 = simplecomponent(key="bbb")
st.write(value1)
value2 = simplecomponent(key="ccc")
st.write(value2)
''')
st.markdown('As you can see, all the information regarding the "mysimplecomponent" component is centralized in the Python file defining the program and nowhere else. Certainly, the code contains some pieces of HTML and JavaScript but in a very lightweight manner. Purists will find a way to "pythonize" the template and the script.')
st.markdown('No template is used, no ReactJS-like framework, no use of npm, no installation of a pip package, no "frontend" directory attached to the Python file defining the component, just the definition of a function that generates an HTML page.')
st.markdown("Yes, but then, if you want to define more sophisticated components (like a dropdown menu, for example), how do you do it? Do you have to reinvent the wheel each time by starting from scratch in HTML?")
st.markdown("The answer is obviously no. There are comprehensive frameworks available on the internet, and furthermore, they are open source, which allow the definition of sophisticated components. An example? Element UI (https://element.eleme.io/#/en-US)")
st.markdown("Element UI notably allows defining components using Vue.js. So, if you've followed me correctly, it's not about reintroducing a template with .vue files, but rather how to generate a single HTML page with Element UI components inside and leveraging Vue.")
st.markdown("I have redefined the function 'gensimplecomponent' and instead created a function 'gencomponent' which relies on Element UI and Vue. This function is as follows:")
st.code('''
def gencomponent(name, template="", script=""):
    def html():
        return f"""
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="UTF-8" />
                    <title>{name}</title>
                    <link rel="stylesheet" href="https://unpkg.com/element-ui/lib/theme-chalk/index.css">
                    <script>
                        function sendMessageToStreamlitClient(type, data) {{
                            const outData = Object.assign({{
                                isStreamlitMessage: true,
                                type: type,
                            }}, data);
                            window.parent.postMessage(outData, "*");
                        }}

                        const Streamlit = {{
                            setComponentReady: function() {{
                                sendMessageToStreamlitClient("streamlit:componentReady", {{apiVersion: 1}});
                            }},
                            setFrameHeight: function(height) {{
                                sendMessageToStreamlitClient("streamlit:setFrameHeight", {{height: height}});
                            }},
                            setComponentValue: function(value) {{
                                sendMessageToStreamlitClient("streamlit:setComponentValue", {{value: value}});
                            }},
                            RENDER_EVENT: "streamlit:render",
                            events: {{
                                addEventListener: function(type, callback) {{
                                    window.addEventListener("message", function(event) {{
                                        if (event.data.type === type) {{
                                            event.detail = event.data
                                            callback(event);
                                        }}
                                    }});
                                }}
                            }}
                        }}
                    </script>

                </head>
            <body>
            {template}
            </body>
            <script src="https://unpkg.com/vue@2/dist/vue.js"></script>
            <script src="https://unpkg.com/element-ui/lib/index.js"></script>
            <script>
                {script}
            </script>
            </html>
        """

    dir = f"{tempfile.gettempdir()}/{name}"
    if not os.path.isdir(dir): os.mkdir(dir)
    fname = f'{dir}/index.html'
    f = open(fname, 'w')
    f.write(html())
    f.close()
    func = components.declare_component(name, path=str(dir))
    def f(**params):
        component_value = func(**params)
        return component_value
    return f
''')
st.markdown('There is no significant difference between "gensinglecomponent" and "gencomponent". Only the inclusion of the libraries we need to create the components differs.')
st.markdown('**Example 1**: Creating a form that returns a set of elements to manipulate in Python.')
showcodeandrun('''
template="""
    <div id="app">
        <el-form ref="form" :model="form" label-width="120px">
            <el-form-item label="Activity name">
                <el-input v-model="form.name" ref="formname" ></el-input>
            </el-form-item>
            <el-form-item label="Activity zone">
                <el-select v-model="form.region" ref="formregion" placeholder="please select your zone">
                    <el-option label="Zone one" value="Paris"></el-option>
                    <el-option label="Zone two" value="London"></el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="Activity time">
                <el-col :span="11">
                    <el-date-picker type="date" ref="formdate1" placeholder="Choisissez une date" v-model="form.date1" style="width: 100%;"></el-date-picker>
                </el-col>
                <el-col class="line" :span="2">-</el-col>
                <el-col :span="11">
                    <el-time-picker ref="formdate2" placeholder="Pick a time" v-model="form.date2" style="width: 100%;"></el-time-picker>
                </el-col>
            </el-form-item>
            <el-form-item label="Instant delivery">
                <el-switch v-model="form.delivery" ref="formdelivery"></el-switch>
            </el-form-item>
            <el-form-item label="Activity type">
                <el-checkbox-group v-model="form.type" ref="formtype">
                    <el-checkbox label="Online activities" name="type"></el-checkbox>
                    <el-checkbox label="Promotion activities" name="type"></el-checkbox>
                    <el-checkbox label="Offline activities" name="type"></el-checkbox>
                    <el-checkbox label="Simple brand exposure" name="type"></el-checkbox>
                </el-checkbox-group>
            </el-form-item>
            <el-form-item label="Resources">
                <el-radio-group v-model="form.resource" ref="formresource">
                    <el-radio label="Sponsor"></el-radio>
                    <el-radio label="Venue"></el-radio>
                </el-radio-group>
            </el-form-item>
            <el-form-item label="Activity form">
                <el-input type="textarea" v-model="form.desc" ref="formdesc"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="getFormValues">Create</el-button>
                <el-button>Cancel</el-button>
            </el-form-item>
        </el-form>
    </div>
"""
script = """
    function onRender(event) {
        if (!window.rendered) {
            console.log("event.detail.args", event.detail.args)
            Streamlit.setFrameHeight(800)
            window.rendered = true
        }
    }
    Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
    Streamlit.setComponentReady()
    const vue = new Vue({
        data: {
            form : {
                name: 'abcd',
                region: '',
                date1: '',
                date2: '',
                delivery: false,
                type: [],
                resource: '',
                desc: ''
            },
        },
        methods: {
            getFormValues (event) {
                console.log(this.$refs.formtype)
                Streamlit.setComponentValue({
                    name: this.$refs.formname.value,
                    region: this.$refs.formregion.value,
                    date1: this.$refs.formdate1.value,
                    date2: this.$refs.formdate2.value,
                    delivery: this.$refs.formdelivery.value,
                    type: this.$refs.formtype.value,
                    resource: this.$refs.formresource.value,
                    desc: this.$refs.formdesc.value,
                })
            }
        },
    }).$mount('#app')
"""

myfrm = gencomponent('myform1',template=template, script=script)
value = myfrm()
st.write('The result in python:', value)

''')
st.markdown('**Example 2**: Another example that defines a dropdown menu from which we want to retrieve the selected item in Python.')
showcodeandrun('''
template="""
<div id="app">
    <el-row class="block-col-2">
        <el-col :span="12">
            <span class="demonstration">hover to trigger</span>
            <el-dropdown @command="handleCommand">
                <span class="el-dropdown-link">
                    Dropdown List<i class="el-icon-arrow-down el-icon--right"></i>
                </span>
                <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item icon="el-icon-plus" command="A1">Action 1</el-dropdown-item>
                    <el-dropdown-item icon="el-icon-circle-plus" command="A2">Action 2</el-dropdown-item>
                    <el-dropdown-item icon="el-icon-circle-plus-outline" command="A3">Action 3</el-dropdown-item>
                    <el-dropdown-item icon="el-icon-check" command="A4">Action 4</el-dropdown-item>
                    <el-dropdown-item icon="el-icon-circle-check" command="A5">Action 5</el-dropdown-item>
            </el-dropdown-menu>
            </el-dropdown>
        </el-col>
        <el-col :span="12">
            <span class="demonstration">click to trigger</span>
            <el-dropdown trigger="click" @command="handleCommand">
                <span class="el-dropdown-link">
                    Dropdown List<i class="el-icon-arrow-down el-icon--right"></i>
                </span>
                <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item icon="el-icon-plus" command="A1">Action 1</el-dropdown-item>
                    <el-dropdown-item icon="el-icon-circle-plus" command="A2">Action 2</el-dropdown-item>
                    <el-dropdown-item icon="el-icon-circle-plus-outline" command="A3">Action 3</el-dropdown-item>
                    <el-dropdown-item icon="el-icon-check" command="A4">Action 4</el-dropdown-item>
                    <el-dropdown-item icon="el-icon-circle-check" command="A5">Action 5</el-dropdown-item>
                </el-dropdown-menu>
            </el-dropdown>
        </el-col>
    </el-row>
</div>
"""
script = """
    function onRender(event) {
        if (!window.rendered) {
            console.log("event.detail.args", event.detail.args)
            Streamlit.setFrameHeight(200)
            window.rendered = true
        }
    }
    Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
    Streamlit.setComponentReady()
    const vue = new Vue({
        data: {
        },
        methods: {
            handleCommand(command) {
                Streamlit.setComponentValue(command)
            }
        }
    }).$mount('#app')
"""

ddwn = gencomponent('Dropdown',template=template, script=script)
value = ddwn()
st.write('The result in python:', value)
''')
st.markdown('In these initial examples, we saw the method for communicating information in the "html page to Python through JavaScript" direction. The method "Streamlit.setComponentValue" is used in the JavaScript code, and the result is not necessarily a simple variable; it can be a structure as shown in the example with the input form.')
st.markdown('Of course, it is possible to communicate information in the other direction (from Python to the HTML page). The parameters passed are visible in JavaScript through the "event.detail.args" object.')
st.markdown('**Example 3**: An uninteresting visual example where parameters passed by Python are retrieved in JavaScript and then returned to Python (A sort of echo where JavaScript is involved).')
showcodeandrun('''
template="""
<div id="app">
</div>
"""
script = """
    function onRender(event) {
        if (!window.rendered) {
            console.log("event.detail.args", event.detail.args)
            Streamlit.setComponentValue(event.detail.args)
            Streamlit.setFrameHeight()
            window.rendered = true
        }
    }
    Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
    Streamlit.setComponentReady()
"""

echo = gencomponent('Echo',template=template, script=script)
value = echo(alpha=1, beta=['x', 'y'], gamma={'a':1, 'b':'xxx'})
st.write('The result in python:', value)
''')
st.markdown('As you can see, 2 additional parameters were automatically generated upon component creation. These are the "default" and "key" parameters.')
st.markdown("**Example 4**: Another more realistic example where a tree defined in Python can be manipulated in HTML with drag and drop capabilities. The HTML page returns certain operations performed on the tree to the Python part.")
showcodeandrun('''
template="""
    <div id="app">
        <el-tree 
            :data="data" 
            node-key="id" 
            default-expand-all 
            @node-click="handleClick" 
            @node-drag-start="handleDragStart" 
            @node-drag-end="handleDragEnd" 
            @node-drop="handleDrop"
            draggable>
        </el-tree>
    </div>    
"""
script = """
    function onRender(event) {
        if (!window.rendered) {
            console.log("event.detail.args", event.detail.args)
            vue.data=event.detail.args.tree;
            Streamlit.setFrameHeight(200)
            window.rendered = true
        }
    }
    Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
    Streamlit.setComponentReady()
    const vue = new Vue({
            data() {
                return {
                    data: [
                    ],
                    defaultProps: {
                        children: 'children',
                        label: 'label'
                    }
                };
            },
        methods: {
            handleClick(node, property) {
                Streamlit.setComponentValue({'event':'click', 'label':node.label});
            },
            handleDragStart(node, event) {
                Streamlit.setComponentValue({'event':'dragstart', 'label':node.data.label});
            },
            handleDragEnd(from, to, type, ev) {
                Streamlit.setComponentValue({'event':'dragend', 'from':from.data.label, 'to':to.data.label, 'where':type})
            },
            handleDrop(from, to, type, ev) {
                Streamlit.setComponentValue({'event':'drag&drop', 'from':from.data.label, 'to':to.data.label, 'where':type})
            },
        }
}).$mount('#app')
"""
tree = gencomponent('tree',template=template, script=script)
treedata = [dict(label='x', children=[dict(label='x_1', children=[]), dict(label='x_2', children=[])]), dict(label='y', children=[]),dict(label='z', children=[])]
value = tree(tree=treedata)
st.write('The result in python:', value)
''')

st.markdown("In conclusion, as you will have understood, my goal is not to deliver ergonomic components usable in Streamlit, but to show that the creation of components can be achieved much more simply than anything I have seen so far. One may certainly disagree with my viewpoint, preferring to create obscure templates, but I am certain that many readers will share my perspective!")
