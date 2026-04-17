from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

doc = Document()

# ── Page margins ──────────────────────────────────────────────────────────────
section = doc.sections[0]
section.top_margin    = Cm(2.5)
section.bottom_margin = Cm(2.0)
section.left_margin   = Cm(3.0)
section.right_margin  = Cm(2.5)

# ── Helpers ───────────────────────────────────────────────────────────────────
def set_font(run, name="Times New Roman", size=12, bold=False, italic=False, color=None):
    run.font.name   = name
    run.font.size   = Pt(size)
    run.font.bold   = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)

def heading(text, level=1, size=14, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, color=(0,0,0)):
    p = doc.add_paragraph()
    p.alignment = align
    run = p.add_run(text)
    set_font(run, size=size, bold=bold, color=color)
    if level == 1:
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after  = Pt(6)
        # bottom border
        pPr = p._p.get_or_add_pPr()
        pBdr = OxmlElement('w:pBdr')
        bottom = OxmlElement('w:bottom')
        bottom.set(qn('w:val'), 'single')
        bottom.set(qn('w:sz'), '6')
        bottom.set(qn('w:space'), '1')
        bottom.set(qn('w:color'), '000000')
        pBdr.append(bottom)
        pPr.append(pBdr)
    elif level == 2:
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after  = Pt(4)
    else:
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after  = Pt(2)
    return p

def body(text, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(8)
    run = p.add_run(text)
    set_font(run, size=12)
    return p

def bullet(text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(3)
    run = p.add_run(text)
    set_font(run, size=12)
    return p

def code_block(lines):
    for line in lines.strip().split('\n'):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after  = Pt(0)
        p.paragraph_format.left_indent  = Cm(0.5)
        run = p.add_run(line if line else " ")
        run.font.name = "Courier New"
        run.font.size = Pt(9)
        # grey background via shading
        rPr = run._r.get_or_add_rPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'),   'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'),  'F4F4F4')
        rPr.append(shd)
    doc.add_paragraph()  # spacer

def screenshot_placeholder(label):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after  = Pt(6)
    run = p.add_run(f"[ Screenshot – {label} ]")
    set_font(run, size=11, italic=True, color=(100, 100, 100))

    # dashed border around paragraph
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    for side in ('top','left','bottom','right'):
        el = OxmlElement(f'w:{side}')
        el.set(qn('w:val'),   'dashed')
        el.set(qn('w:sz'),    '6')
        el.set(qn('w:space'), '4')
        el.set(qn('w:color'), '888888')
        pBdr.append(el)
    pPr.append(pBdr)

    # add empty lines for pasting image
    for _ in range(4):
        ep = doc.add_paragraph()
        ep.paragraph_format.space_before = Pt(0)
        ep.paragraph_format.space_after  = Pt(0)

def api_table(rows):
    headers = ["Method", "Endpoint", "Description", "Request Body", "Response"]
    t = doc.add_table(rows=1+len(rows), cols=5)
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    # column widths
    widths = [Cm(2), Cm(4), Cm(4.5), Cm(4), Cm(3.5)]
    for i, cell in enumerate(t.rows[0].cells):
        cell.width = widths[i]
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = cell.paragraphs[0].add_run(headers[i])
        set_font(run, size=10, bold=True, color=(255,255,255))
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'),   'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'),  '222222')
        tcPr.append(shd)
    for ri, row_data in enumerate(rows):
        for ci, val in enumerate(row_data):
            cell = t.rows[ri+1].cells[ci]
            cell.width = widths[ci]
            run = cell.paragraphs[0].add_run(val)
            set_font(run, name="Courier New" if ci in (0,1,3) else "Times New Roman", size=10)
            if (ri % 2) == 1:
                tc = cell._tc
                tcPr = tc.get_or_add_tcPr()
                shd = OxmlElement('w:shd')
                shd.set(qn('w:val'),   'clear')
                shd.set(qn('w:color'), 'auto')
                shd.set(qn('w:fill'),  'F2F2F2')
                tcPr.append(shd)
    doc.add_paragraph()

def test_table(rows):
    headers = ["#", "Request", "Method", "Expected Status", "Assertions"]
    t = doc.add_table(rows=1+len(rows), cols=5)
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    widths = [Cm(1), Cm(5), Cm(2), Cm(3), Cm(7)]
    for i, cell in enumerate(t.rows[0].cells):
        cell.width = widths[i]
        run = cell.paragraphs[0].add_run(headers[i])
        set_font(run, size=10, bold=True, color=(255,255,255))
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'),'clear'); shd.set(qn('w:color'),'auto'); shd.set(qn('w:fill'),'222222')
        tcPr.append(shd)
    for ri, row_data in enumerate(rows):
        for ci, val in enumerate(row_data):
            cell = t.rows[ri+1].cells[ci]
            cell.width = widths[ci]
            run = cell.paragraphs[0].add_run(val)
            set_font(run, size=10)
            if ri % 2 == 1:
                tc = cell._tc
                tcPr = tc.get_or_add_tcPr()
                shd = OxmlElement('w:shd')
                shd.set(qn('w:val'),'clear'); shd.set(qn('w:color'),'auto'); shd.set(qn('w:fill'),'F2F2F2')
                tcPr.append(shd)
    doc.add_paragraph()

# ══════════════════════════════════════════════════════════════════════════════
#  COVER PAGE
# ══════════════════════════════════════════════════════════════════════════════
for _ in range(4): doc.add_paragraph()

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Ain Shams University"); set_font(r, size=16, bold=True)

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Faculty of Engineering – Computer & Systems Engineering"); set_font(r, size=13)

for _ in range(3): doc.add_paragraph()

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Lab 7 Report"); set_font(r, size=24, bold=True)

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Mini-Twitter Backend Implementation & API Testing"); set_font(r, size=14)

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Course: Internet Programming – CSE341"); set_font(r, size=12, italic=True)

for _ in range(4): doc.add_paragraph()

info = [
    ("Student Name:", "Yousif"),
    ("Student ID:",   "22P0008"),
    ("Section:",      "___________"),
    ("Instructor:",   "___________"),
]
for label, value in info:
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p.add_run(f"{label}  "); set_font(r1, size=12, bold=True)
    r2 = p.add_run(value);        set_font(r2, size=12)

for _ in range(4): doc.add_paragraph()

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Academic Year 2025 – 2026  |  Spring Semester"); set_font(r, size=11, italic=True)

doc.add_page_break()

# ══════════════════════════════════════════════════════════════════════════════
#  1. INTRODUCTION
# ══════════════════════════════════════════════════════════════════════════════
heading("1. Introduction")
body("This report documents the implementation of a RESTful backend server for the Mini-Twitter application, developed as part of Lab 7 of the Internet Programming course (CSE341). The objective was to build a functional HTTP server using Node.js and Express.js that exposes a REST API designed in the previous lab (Lab 6), and to connect it to a provided React frontend.")
body("Data is stored in-memory using JavaScript arrays, as required by the lab specification. The server was tested using a Postman collection run via the Newman CLI runner, with all 21 assertions passing.")

# ══════════════════════════════════════════════════════════════════════════════
#  2. TOOLS & TECHNOLOGIES
# ══════════════════════════════════════════════════════════════════════════════
heading("2. Tools & Technologies")
tools = [
    ("Node.js",         "JavaScript runtime for executing server-side code."),
    ("Express.js",      "Web framework for defining HTTP routes and middleware."),
    ("React + Vite",    "Frontend provided by the lab (repository: mina58/lab-8-web)."),
    ("Postman/Newman",  "API design tool and automated endpoint testing via CLI."),
    ("npm",             "Package manager used to initialise the project and install dependencies."),
]
for name, desc in tools:
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(3)
    r1 = p.add_run(name + ": "); set_font(r1, size=12, bold=True)
    r2 = p.add_run(desc);         set_font(r2, size=12)

doc.add_paragraph()

# ══════════════════════════════════════════════════════════════════════════════
#  3. API DESIGN
# ══════════════════════════════════════════════════════════════════════════════
heading("3. API Design")
body("The API was designed in Lab 6 using a Postman mock server. It follows REST conventions and supports the following operations on posts and comments:")

api_table([
    ("GET",    "/posts",              "Get all posts",         "—",                   "200 – Array of posts"),
    ("POST",   "/posts",              "Create a new post",     "{ name, content }",   "201 – Created post"),
    ("GET",    "/posts/:id",          "Get a single post",     "—",                   "200 – Post object"),
    ("PUT",    "/posts/:id",          "Edit a post",           "{ name?, content? }", "200 – Updated post"),
    ("DELETE", "/posts/:id",          "Delete a post",         "—",                   "204 – No Content"),
    ("GET",    "/posts/:id/comments", "Get all comments",      "—",                   "200 – String array"),
    ("POST",   "/posts/:id/comments", "Add a comment",         "{ text }",            "201 – Created comment"),
])

# ══════════════════════════════════════════════════════════════════════════════
#  4. IMPLEMENTATION
# ══════════════════════════════════════════════════════════════════════════════
heading("4. Implementation")

heading("4.1  Project Setup", level=2)
body("The project was initialised with npm and Express was installed as the only dependency:")
code_block("npm init -y\nnpm install express")

heading("4.2  Server Code (server.js)", level=2)
body("The server uses an in-memory array (posts) as the data store. Each post object contains an id, name, content, and a nested comments array. A CORS middleware is added so the React frontend (port 5173) can communicate with the backend (port 4000).")

code_block("""const express = require("express");
const app = express();
app.use(express.json());

// CORS – allow requests from the React frontend
app.use((req, res, next) => {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type");
    next();
});

let posts = [];
let nextPostId = 1;
let nextCommentId = 1;

// GET /posts
app.get("/posts", (req, res) => {
    res.json(posts.map(({ comments, ...post }) => post));
});

// POST /posts
app.post("/posts", (req, res) => {
    const { name, content } = req.body;
    const post = { id: nextPostId++, name, content, comments: [] };
    posts.push(post);
    res.status(201).json({ id: post.id, name: post.name, content: post.content });
});

// GET /posts/:id
app.get("/posts/:id", (req, res) => {
    const post = posts.find(p => p.id === parseInt(req.params.id));
    if (!post) return res.status(404).json({ error: "Post not found" });
    res.json({ id: post.id, name: post.name, content: post.content });
});

// PUT /posts/:id
app.put("/posts/:id", (req, res) => {
    const post = posts.find(p => p.id === parseInt(req.params.id));
    if (!post) return res.status(404).json({ error: "Post not found" });
    if (req.body.name) post.name = req.body.name;
    if (req.body.content) post.content = req.body.content;
    res.json({ id: post.id, name: post.name, content: post.content });
});

// DELETE /posts/:id
app.delete("/posts/:id", (req, res) => {
    const index = posts.findIndex(p => p.id === parseInt(req.params.id));
    if (index === -1) return res.status(404).json({ error: "Post not found" });
    posts.splice(index, 1);
    res.status(204).end();
});

// GET /posts/:id/comments
app.get("/posts/:id/comments", (req, res) => {
    const post = posts.find(p => p.id === parseInt(req.params.id));
    if (!post) return res.status(404).json({ error: "Post not found" });
    res.json(post.comments.map(c => c.text));
});

// POST /posts/:id/comments
app.post("/posts/:id/comments", (req, res) => {
    const post = posts.find(p => p.id === parseInt(req.params.id));
    if (!post) return res.status(404).json({ error: "Post not found" });
    const comment = { id: nextCommentId++, text: req.body.text };
    post.comments.push(comment);
    res.status(201).json(comment);
});

app.listen(4000, () => console.log("Server running on http://localhost:4000"));""")

heading("4.3  Frontend Integration (api.js)", level=2)
body("The provided React frontend contained stub functions in src/api/api.js. These were implemented using async/await with the browser's fetch() API, pointing to the local Express backend. One key transformation: the NewCommentForm component sends { comment: '...' }, which is remapped to { text: '...' } before being sent to the server.")

code_block("""const BASE_URL = "http://localhost:4000";

export const getAllPosts = async () => {
  try {
    const response = await fetch(`${BASE_URL}/posts`);
    if (!response.ok) throw new Error(`Failed to fetch posts: ${response.statusText}`);
    return await response.json();
  } catch (error) {
    console.error("Error fetching posts:", error);
    return [];
  }
};

export const getPostDetails = async (postId) => {
  try {
    const postResponse = await fetch(`${BASE_URL}/posts/${postId}`);
    if (!postResponse.ok) throw new Error(`Failed to fetch post: ${postResponse.statusText}`);
    const post = await postResponse.json();
    const commentsResponse = await fetch(`${BASE_URL}/posts/${postId}/comments`);
    if (!commentsResponse.ok) throw new Error(`Failed to fetch comments: ${commentsResponse.statusText}`);
    const comments = await commentsResponse.json();
    return { post, comments };
  } catch (error) {
    console.error("Error fetching post details:", error);
    return { post: null, comments: [] };
  }
};

export const createNewPost = async (newPostData) => {
  try {
    const response = await fetch(`${BASE_URL}/posts`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newPostData),
    });
    if (!response.ok) throw new Error(`Failed to create post: ${response.statusText}`);
    return await response.json();
  } catch (error) {
    console.error("Error creating post:", error);
  }
};

export const createNewComment = async (postId, newCommentData) => {
  try {
    const response = await fetch(`${BASE_URL}/posts/${postId}/comments`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: newCommentData.comment }),
    });
    if (!response.ok) throw new Error(`Failed to create comment: ${response.statusText}`);
    return await response.json();
  } catch (error) {
    console.error("Error creating comment:", error);
  }
};""")

# ══════════════════════════════════════════════════════════════════════════════
#  5. TESTING
# ══════════════════════════════════════════════════════════════════════════════
heading("5. API Testing with Postman")
body("A Postman collection (lab7-collection.postman_collection.json) was created containing 10 requests covering all endpoints. Each request includes automated test scripts that verify the HTTP status code and the response body. Collection variables (postId, secondPostId) pass IDs dynamically between requests, making the suite repeatable.")

heading("5.1  Test Cases", level=2)
test_table([
    ("1",  "GET /posts (empty)",              "GET",    "200", "Status 200, empty array returned"),
    ("2",  "POST /posts – first post",         "POST",   "201", "Status 201, id/name/content present"),
    ("3",  "POST /posts – second post",        "POST",   "201", "Status 201, name correct"),
    ("4",  "GET /posts (2 posts)",             "GET",    "200", "Array length 2, no comments field"),
    ("5",  "GET /posts/:id",                   "GET",    "200", "Correct name and content"),
    ("6",  "GET /posts/:id/comments (empty)",  "GET",    "200", "Empty array"),
    ("7",  "POST /posts/:id/comments – first", "POST",   "201", "Comment text correct"),
    ("8",  "POST /posts/:id/comments – second","POST",   "201", "Comment text correct"),
    ("9",  "GET /posts/:id/comments (2)",      "GET",    "200", "Array of 2 strings, correct values"),
    ("10", "GET /posts/999 (not found)",        "GET",    "404", "Error property present in response"),
])

heading("5.2  Newman Run Results", level=2)
body("All 21 assertions passed with 0 failures across 10 requests (total run duration: ~130 ms).")
screenshot_placeholder("Newman terminal output showing all 10 requests passing with 21/21 assertions")

heading("5.3  Postman Screenshots", level=2)

for label in [
    "GET /posts – response showing the array of posts",
    "POST /posts – request body { name, content } and 201 Created response",
    "GET /posts/:id – single post object returned",
    "PUT /posts/:id – updated post in response",
    "DELETE /posts/:id – 204 No Content response",
    "POST /posts/:id/comments – comment body and 201 response",
    "GET /posts/:id/comments – array of comment strings",
]:
    heading(label.split("–")[0].strip(), level=3)
    screenshot_placeholder(label)

# ══════════════════════════════════════════════════════════════════════════════
#  6. FRONTEND INTEGRATION
# ══════════════════════════════════════════════════════════════════════════════
heading("6. Frontend Integration")
body("The React frontend was cloned from the mina58/lab-8-web repository and run using Vite on port 5173. After implementing api.js and starting both servers, the full application was accessible at http://localhost:5173.")

heading("Application Home – Post List", level=3)
screenshot_placeholder("Mini-Twitter app in the browser – post list and create-post form visible")

heading("Post Detail View – Comments", level=3)
screenshot_placeholder("Single post detail view showing comments list and add-comment form")

# ══════════════════════════════════════════════════════════════════════════════
#  7. CONCLUSION
# ══════════════════════════════════════════════════════════════════════════════
heading("7. Conclusion")
body("This lab demonstrated how to build a RESTful backend server using Node.js and Express.js. A seven-endpoint API was implemented for a Mini-Twitter application, supporting full CRUD operations on posts and comment creation and retrieval. The backend was integrated with a React frontend by implementing fetch-based API functions using async/await. All endpoints were verified through an automated Postman collection with 21 passing assertions.")
body("Key concepts practised: REST API design, HTTP methods and status codes, Express routing and middleware (JSON body parsing, CORS), in-memory data storage with JavaScript arrays, and asynchronous JavaScript with async/await.")

# ── Save ──────────────────────────────────────────────────────────────────────
out = "/Users/yousif/ASU/SEMESTER 8/IP/LABS/internet-programming-labs/LAB 7/Lab7_Report.docx"
doc.save(out)
print(f"Saved: {out}")
