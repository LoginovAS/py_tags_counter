#!/usr/bin/env python3.5

import time
import json
from rq import Queue, get_failed_queue
from rq.job import Job
from redis import Redis
from flask import Flask, jsonify, abort
from flask import make_response, request, url_for
import requests
from lxml import html
from collections import Counter
import tasks
from status import JobStatus

app = Flask(__name__)

@app.route('/v1/test_task', methods=['POST'])
def create_test_task():
    redis_conn = Redis();
    queue = Queue(connection = redis_conn)
    job = queue.enqueue('tasks.test_task')
    return jsonify({'task_uuid':job.id}), 201

@app.route('/v1/test_task', methods=['GET'])
def get_test_task():
    job_id = request.json['task_uuid']
    redis_conn = Redis();
    job = Job.fetch(job_id,connection = redis_conn)

    # if job.is_failed:
    #     fq = get_failed_queue()
    #     return jsonify({'Status':JobStatus.ERROR.value,'Result':job.result}), 204

    if job.is_finished:
        return jsonify({'Status':JobStatus.DONE.value,'Result':job.result}), 200

    if job.is_started:
        return jsonify({'Status':JobStatus.RUNNING.value,'Result':''}), 200

    if job.is_queued:
        return jsonify({'Status':JobStatus.QUEUED.value,'Result':''}), 200

@app.route('/v1/task', methods=['POST'])
def create_task():
    url = request.json['url']
    redis_conn = Redis();
    queue = Queue(connection = redis_conn)
    job = queue.enqueue('tasks.count_tags_in_url', url, result_ttl=5000)
    return jsonify({'task_uuid':job.id}), 201

@app.route('/v1/task', methods=['GET'])
def get_task():
    job_id = request.json['task_uuid']
    redis_conn = Redis();
    job = Job.fetch(job_id,connection = redis_conn)

    # if job.is_failed:
    #     fq = get_failed_queue()
    #     return jsonify({'Status':JobStatus.ERROR.value,'Result':job.result}), 204

    if job.is_finished:
        return jsonify({'Status':JobStatus.DONE.value,'Result':job.result}), 200

    if job.is_started:
        return jsonify({'Status':JobStatus.RUNNING.value,'Result':''}), 200

    if job.is_queued:
        return jsonify({'Status':JobStatus.QUEUED.value,'Result':''}), 200


@app.errorhandler(404)
def not_found(error):
    return make_response(
        jsonify(
            {'error': 'Not found'}
        ), 404
    )

@app.errorhandler(400)
def bad_request(error):
    return make_response(
        jsonify(
            {'error': 'Bad Request'}
        ), 400
    )

if __name__ == '__main__':
    app.run(debug = True)
