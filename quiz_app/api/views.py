from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from .serializers import QuizSerializer
from ..models import Quiz
import whisper
from google import genai
import json, re
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import mixins, viewsets
from .permissions import isCreatorOrReadOnly
import os
from dotenv import load_dotenv
load_dotenv()

class QuizCreateView(generics.CreateAPIView):
    """
    API endpoint for creating Quizzes.
    Accepts a video URL, processes the video to generate a quiz using transcription and AI,
    and returns the created Quiz object with its questions.
    """
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]
    device = "cpu"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        url = serializer.validated_data["video_url"]

        import tempfile, yt_dlp, os
        from ..models import Question

        with tempfile.TemporaryDirectory() as tmpdir:
            ydl_opts = {
                "js_runtimes": {
                    "node": {}
                },
                "remote_components": [
                    "ejs:github"
                ],
                "format": "bestaudio/best",
                "outtmpl": os.path.join(tmpdir, "audio.%(ext)s"),
                "quiet": True,
                "noplaylist": True,
                "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                audio_file = info["requested_downloads"][0]["filepath"]

            model = whisper.load_model("turbo")
            results = model.transcribe(audio_file)
            transcript_text = " ".join([segment["text"] for segment in results["segments"]])

            client = genai.Client(api_key=os.getenv("GENAI_API_KEY", default="unsecure-key"))

            prompt = f"""
                Based on the following transcript, generate a quiz in valid JSON format.
                The quiz must follow this exact structure:
                    {{
                    "title": "Create a concise quiz title based on the topic of the transcript.",
                    "description": "Summarize the transcript in no more than 150 characters. Do not include any quiz questions or answers.",
                    "questions": [
                        {{
                        "question_title": "The question goes here.",
                        "question_options": ["Option A", "Option B", "Option C", "Option D"],
                        "answer": "The correct answer from the above options"
                        }},
                        ...
                        (exactly 10 questions)
                    ]
                    }}
                Requirements:
                - Each question must have exactly 4 distinct answer options.
                - Only one correct answer is allowed per question, and it must be present in 'question_options'.
                - The output must be valid JSON and parsable as-is (e.g., using Python's json.loads).
                - Do not include explanations, comments, or any text outside the JSON.
                
                TRANSCRIPT:
                {transcript_text}
                """
            
            response = client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=prompt,
            )
            
            raw = response.candidates[0].content.parts[0].text
            json_str = re.search(r"\{.*\}", raw, re.S).group()
            quiz_data = json.loads(json_str)
    
            quiz = serializer.save(
                creator=request.user,
                title=quiz_data["title"],
                description=quiz_data["description"],
                video_url=url,
            )

            for q in quiz_data["questions"]:
                Question.objects.create(
                    quiz=quiz,
                    question_title=q["question_title"],
                    question_options=q["question_options"],
                    answer=q["answer"],
                )

            output_serializer = QuizSerializer(quiz)

            return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class ListRetrieveUpdateDestroyViewSet(
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.DestroyModelMixin,
                                mixins.UpdateModelMixin,
                                viewsets.GenericViewSet):
    """
    Custom ViewsetClass for further use.
    """
    pass

class QuizViewSet(ListRetrieveUpdateDestroyViewSet):
    """
    API endpoint for view of Quizzes.

    Lists Quizzes where the user is authenticated user,
    and allows updating, creating, deleting a quiz where the requesting user is set as the creator who made the quiz.
    """
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [isCreatorOrReadOnly]