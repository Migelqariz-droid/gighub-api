from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Literal
app = FastAPI(
    title="GigHub API",
    description="API for managing freelance gigs in Nyeri.\nAdmission Number: C027-01-0896/2024",
    version="1.0.0",
    docs_url="/swagger",
    redoc_url=None, 
    openapi_url="/openapi.json",
)

gigs_db = [
    {
        "id": 1,
        "title": "Potrait Photography",
        "description": "Create retouched potraits.",
        "category": "Development",
        "budget": 9000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Marylyn Mambo"
    },
    {
        "id": 2,
        "title": "Film Editor",
        "description": "Edit a nice vintage action film.",
        "category": "Development",
        "budget": 22000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "John Kinuthia"
    },
    {
        "id": 3,
        "title": "Animation",
        "description": "Provide nice animations for a food cafe advert.",
        "category": "Design",
        "budget": 30000.0,
        "currency": "KES",
        "status": "In Progress",
        "client_name": "Chris Hamnes"
    },
    {
        "id": 4,
        "title": "Script writing",
        "description": "Review script written for a school flix.",
        "category": "Writing",
        "budget": 10000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Caleb Kinyua"
    },
    {
        "id": 5,
        "title": "Poster Adverts Design",
        "description": "Design nice poster marketing a film class",
        "category": "Design",
        "budget": 12000.0,
        "currency": "KES",
        "status": "Closed",
        "client_name": "Phillip Mbugua"
    },
    {
        "id": 6,
        "title": "Ai Movie Creation",
        "description": "Develop a nice ai superheroe movie.",
        "category": "Development",
        "budget": 57000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Lorna Theuri"
    },
    {
        "id": 7,
        "title": "Shoot setup",
        "description": "Develop a nice 3 point light shooting setup.",
        "category": "Development",
        "budget": 14000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "John Wambua"
    },
    {
     	"id": 8,
    	"title": "Cinematography",
    	"description": "Capture high-quality footage for a short documentary using professional camera equipment.",
    	"category": "Development",
    	"budget": 35000.0,
    	"currency": "KES",
    	"status": "Open",
    	"client_name": "Brian Mwangi"
    },
    {
    	"id": 9,
    	"title": "Screenplay Writing",
    	"description": "Write a compelling screenplay for a thirty-minute drama film with engaging dialogue.",
    	"category": "Writing",
    	"budget": 28000.0,
    	"currency": "KES",
    	"status": "Open",
    	"client_name": "Faith Wanjiru"
    },
    {
    	"id": 10,
    	"title": "Movie Poster Design",
    	"description": "Design an attractive promotional poster for an upcoming independent feature film release.",
    	"category": "Design",
    	"budget": 15000.0,
    	"currency": "KES",
    	"status": "In Progress",
    	"client_name": "Kevin Kariuki"
    },
    {
    	"id": 11,
    	"title": "Video Editing",
    	"description": "Edit raw film footage into a polished short film with smooth transitions and sound effects.",
    	"category": "Development",
    	"budget": 40000.0,
    	"currency": "KES",
    	"status": "Open",
    	"client_name": "Grace Njeri"
     },
     {
    	"id": 12,
    	"title": "Subtitle Writing",
    	"description": "Create accurate English subtitles and captions for a feature-length documentary film.",
    	"category": "Writing",
    	"budget": 18000.0,
    	"currency": "KES",
    	"status": "Closed",
    	"client_name": "Daniel Kimani"

      },
]
class GigCreate(BaseModel):
    title: str = Field(min_length=5, max_length=100)
    description: str = Field(min_length=20, max_length=500)
    category: Literal["Development", "Writing", "Design"]
    budget: float = Field(gt=0)
    client_name: str = Field(min_length=2, max_length=50)


class GigUpdate(BaseModel):
    budget: Optional[float] = Field(None, gt=0)
    status: Optional[Literal["Open", "In Progress", "Closed"]] = None



@app.get("/gigs")
def get_gigs():
    """
    Return all gigs.
    """
    return gigs_db




@app.get("/gigs/{gig_id}")
def get_gig(gig_id: int):
    """
    Return a single gig by ID.
    """
    for gig in gigs_db:
        if gig["id"] == gig_id:
            return gig

    raise HTTPException(status_code=404, detail="Gig not found")


@app.get("/gigs/search")
def search_gigs(q: str):
    """
    Search gigs by title.
    """
    results = []

    for gig in gigs_db:
        if q.lower() in gig["title"].lower():
            results.append(gig)

    return results



@app.post("/gigs")
def create_gig(gig: GigCreate):
    """
    Create a new gig.
    """

    new_id = max([g["id"] for g in gigs_db]) + 1

    new_gig = {
        "id": new_id,
        "title": gig.title,
        "description": gig.description,
        "category": gig.category,
        "budget": gig.budget,
        "currency": "KES",
        "status": "Open",
        "client_name": gig.client_name
    }

    gigs_db.append(new_gig)

    return {
        "message": "Gig created successfully",
        "gig": new_gig
    }
@app.put("/gigs/{gig_id}")
def update_gig(gig_id: int, gig_update: GigUpdate):
    """
    Update a gig's budget or status.
    """

    for index, gig in enumerate(gigs_db):

        if gig["id"] == gig_id:

            if gig_update.budget is not None:
                gigs_db[index]["budget"] = gig_update.budget

            if gig_update.status is not None:
                gigs_db[index]["status"] = gig_update.status

            return {
                "message": "Gig updated successfully",
                "gig": gigs_db[index]
            }

    raise HTTPException(status_code=404, detail="Gig not found")
@app.delete("/gigs/{gig_id}")
def delete_gig(gig_id: int):
    """
    Delete a gig.
    """

    for index, gig in enumerate(gigs_db):

        if gig["id"] == gig_id:

            deleted_gig = gigs_db.pop(index)

            return {
                "message": "Gig deleted successfully",
                "gig": deleted_gig
            }

    raise HTTPException(status_code=404, detail="Gig not found")