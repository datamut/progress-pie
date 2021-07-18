FROM python:3.8.11-alpine

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /code
RUN chown appuser:appgroup -R .

USER appuser

COPY --chown=appuser:appgroup . .
WORKDIR /code

RUN python -m venv venv
ENV PATH "/code/venv/bin:$PATH"
RUN python -m pip install --upgrade pip

RUN pip install -r requirements_test.txt

CMD ["pytest", "progress_pie/tests", "--cov=progress_pie"]
